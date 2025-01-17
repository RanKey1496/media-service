import asyncio
import nats
import json

async def main():
    try:
        nc = await nats.connect("nats://127.0.0.1:4222")

        
        data = {"id": 2, "source": "instagram", "data": {"type": "url", "urls": [
            "https://www.instagram.com/reel/DEkG_ZnOKdk/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
            "https://www.instagram.com/reel/DEPpicXx96f/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
            "https://www.instagram.com/reel/DEM4lCHO1XI/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
            ]}}
        #data = {"id": 1, "source": "instagram", "data": {"type": "profile", "username": "brazilian_301", "first_n_posts": 5, "random_n_posts": 3}}
        await nc.publish("job.media.created", json.dumps(data).encode())
        await nc.drain()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())