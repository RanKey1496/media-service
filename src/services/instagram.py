import os
import random
from utils import print_info, print_success, print_error
from instaloader import Instaloader, Profile, Post

class Instagram:
    
    def __init__(self):
        self._instaloader = Instaloader(dirname_pattern='videos/{profile}/{target}', filename_pattern='{target}')
    
    def get_profile(self, username):
        return Profile.from_username(self._instaloader.context, username)
    
    def download_posts(self, posts):
        filepaths = []
        for post in posts:
            output = f'{post.shortcode}'
            self._instaloader.download_post(post, target=output)
            filepaths.append(os.path.join('videos', post.profile, output, output + '.mp4'))
        return filepaths
    
    def get_random_n_posts(self, profile, first_n_posts=10, random_n_posts=5):
        print_info(f"Downloading {random_n_posts} random posts from {profile.username}...")
        posts = profile.get_posts()
        n_posts = []
        i = 0
        
        while i < first_n_posts:
            try:
                post = posts.__next__()
                if post.is_video and str.lower(post.owner_username) == str.lower(profile.username):
                    n_posts.append(post)
                    i += 1
            except StopIteration:
                break
            
        all_posts = list(n_posts)
        total_posts = len(all_posts)
        
        if total_posts == 0:
            return []
        
        if total_posts < random_n_posts:
            random_n_posts = total_posts
            
        random_index = random.sample(range(total_posts), random_n_posts)
        selected_posts = [all_posts[i] for i in random_index]
        
        return selected_posts
    
    def get_posts_from_url(self, urls):
        print_info(f"Downloading {len(urls)} posts from urls...")
        #Validar que sean urls validas
        #Validar que los posts sean videos
        
        posts = []
        for url in urls:
            post = Post.from_shortcode(self._instaloader.context, url.split("/")[-2])
            posts.append(post)
            
        return posts
    
    def get_posts(self, data):
        # data: {type: ..., url: ..., username: ..., first_n_posts: ..., random_n_posts: ...}
        
        if data['type'] == 'url':
            posts = self.get_posts_from_url(data['urls'])
            return self.download_posts(posts)
        elif data['type'] == 'profile':
            posts = self.get_random_n_posts(self.get_profile(data['username']), data['first_n_posts'], data['random_n_posts'])
            return self.download_posts(posts)
        else:
            return []