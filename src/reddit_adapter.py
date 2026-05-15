#!/usr/bin/env python3
"""
Reddit adapter for DuplicateDestroyer
Enables cross-post and repost detection on Reddit
"""

import praw
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class RedditPost:
    id: str
    title: str
    selftext: str
    url: str
    created_utc: float
    subreddit: str
    author: str
    score: int
    num_comments: int


class RedditAdapter:
    """Adapter to fetch and normalize Reddit posts for duplicate detection."""

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def fetch_posts(self, subreddit: str, limit: int = 100, time_filter: str = "day") -> List[RedditPost]:
        """Fetch recent posts from a subreddit."""
        posts = []
        for submission in self.reddit.subreddit(subreddit).top(time_filter=time_filter, limit=limit):
            posts.append(RedditPost(
                id=submission.id,
                title=submission.title,
                selftext=submission.selftext,
                url=submission.url,
                created_utc=submission.created_utc,
                subreddit=str(submission.subreddit),
                author=str(submission.author),
                score=submission.score,
                num_comments=submission.num_comments,
            ))
        return posts

    def check_duplicate(self, post: RedditPost, existing: List[RedditPost], threshold: float = 0.85) -> List[dict]:
        """Check if a post is a duplicate of existing posts."""
        duplicates = []
        for existing_post in existing:
            similarity = self._compute_similarity(post, existing_post)
            if similarity >= threshold:
                duplicates.append({
                    "original": existing_post,
                    "similarity": similarity,
                })
        return duplicates

    def _compute_similarity(self, post1: RedditPost, post2: RedditPost) -> float:
        """Compute similarity between two posts (placeholder for actual implementation)."""
        # Title similarity (basic)
        title1_words = set(post1.title.lower().split())
        title2_words = set(post2.title.lower().split())
        if not title1_words or not title2_words:
            return 0.0
        intersection = title1_words & title2_words
        union = title1_words | title2_words
        return len(intersection) / len(union)
