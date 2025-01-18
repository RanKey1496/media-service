import os
import asyncio
import utils
import json
import shutil
from services.s3 import S3
from services.nat import Broker
from services.instagram import Instagram
from config import (get_nats_url, get_s3_region, get_s3_bucket, get_s3_key, get_s3_secret)

class Main:
    
    def __init__(self):
        self._s3 = S3(get_s3_region(), get_s3_key(), get_s3_secret())
        self._nats = Broker()
        self._instagram = Instagram()
    
    async def job_media_created_handler(self, msg):
        utils.print_info(f"Received a message on '{msg.subject}': {msg.data.decode()}")
        data = json.loads(msg.data.decode())
        
        if data['source'] == 'instagram':
            utils.print_info("Downloading media from Instagram...")
            outputs = self._instagram.get_posts(data['data'])
            filepaths = self._s3.upload_files(data['id'], outputs, get_s3_bucket())
            [shutil.rmtree(os.path.join('media', os.path.dirname(file))) for file in outputs if os.path.exists(file)]
            await self.job_media_completed_publisher(data['id'], filepaths)
        
        if data['source'] == 'youtube':
            utils.print_info("Downloading media from YouTube...")
            pass
        
    async def job_media_completed_publisher(self, id, filepaths):
        utils.print_info("Publishing media completed...")
        data = json.dumps({"id": id, "media": filepaths}).encode()
        await self._nats.publish("job.media.completed", data)
    
    async def run(self):
        await self._nats.connect(get_nats_url())
        await self._nats.subscribe("job.media.created", self.job_media_created_handler)
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    main_app = Main()
    try:
        loop.run_until_complete(main_app.run())
    except KeyboardInterrupt:
        print("Shutting down...")