import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env 
load_dotenv()

CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if CLAUDE_API_KEY is None:
    raise ValueError("CLAUDE_API_KEY is not set in the environment variables")

headers = {
    "Content-Type": "application/json",
    "x-api-key": CLAUDE_API_KEY,
    "anthropic-version": "2023-06-01"
}

def claude_completion(prompt, max_tokens=1000):
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(CLAUDE_API_URL, json=data, headers=headers)
    response.raise_for_status()
    return response.json()['content'][0]['text']

class Agent:
    def __init__(self, name):
        self.name = name

    def run(self, prompt):
        return claude_completion(prompt)

# Create agents
blog_post_generator = Agent("BlogPostGenerator")
seo_checker = Agent("SEOChecker")
blog_post_refiner = Agent("BlogPostRefiner")

# Workflow function
def create_social_media_post(points):
    # Generate blog post
    blog_post_prompt = "Create a blog post based on the following points:\n" + "\n".join(points)
    blog_post = blog_post_generator.run(blog_post_prompt)
    
    # Check SEO (single turn)
    seo_prompt = f"Provide SEO feedback for the following blog post. Be concise and specific:\n{blog_post}"
    seo_feedback = seo_checker.run(seo_prompt)
    
    # Refine blog post based on SEO feedback
    refine_prompt = f"Rewrite the following blog post to incorporate the SEO feedback. Focus on making the changes suggested in the feedback without altering the core message:\n\nOriginal Blog Post:\n{blog_post}\n\nSEO Feedback:\n{seo_feedback}"
    refined_blog_post = blog_post_refiner.run(refine_prompt)
    
    return {
        "original_post": blog_post,
        "seo_feedback": seo_feedback,
        "refined_post": refined_blog_post
    }

# Workflow
points = [
    "[point 1 eg new way of learning]",
    "Students reported 80% more engagement in learning",
    "Seeing 3D worlds pop up in front of them",
    "Starting 9th Aug 2024"
]

try:
    result = create_social_media_post(points)

    print("Original Blog Post:")
    print(result["original_post"])
    print("\nSEO Feedback:")
    print(result["seo_feedback"])
    print("\nRefined Blog Post:")
    print(result["refined_post"])
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error occurred: {e}")
    print(f"Response content: {e.response.content}")
except Exception as e:
    print(f"An error occurred: {e}")
