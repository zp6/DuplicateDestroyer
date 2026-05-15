# DuplicateDestroyer - Reddit Port Proposal

## Overview
Proposal to port DuplicateDestroyer (a Stack Overflow duplicate question detector) to Reddit for cross-post and repost detection.

## Architecture

### Current (Stack Overflow)
- Ingests Stack Exchange API data
- Uses title + body similarity matching
- Generates duplicate reports
- Tags questions as duplicates

### Proposed (Reddit)
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Reddit API    │───>│  Text         │───>│  Similarity  │
│ (PRAW)        │    │  Preprocessor │    │  Engine      │
└──────────────┘    └──────────────┘    └──────────────┘
                            │                    │
                            v                    v
                    ┌──────────────┐    ┌──────────────┐
                    │  Subreddit   │    │  Duplicate   │
                    │  Config      │    │  Report      │
                    └──────────────┘    └──────────────┘
```

## Reddit-Specific Adaptations

### Data Model
```python
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
```

### Similarity Thresholds
- Title only: 0.85 (Reddit titles carry more weight)
- Title + body: 0.75
- URL match: 0.95 (exact URL = auto-duplicate)

### Reddit API Considerations
- Rate limits: 60 requests/min (OAuth)
- Use PRAW for API access
- Respect subreddit-specific rules
- Bot accounts need moderator approval

### Deployment Options
1. **Reddit Bot**: Runs as a Reddit bot, comments on detected duplicates
2. **Moderator Tool**: Dashboard for subreddit mods to review
3. **Browser Extension**: Real-time duplicate detection while composing

## Next Steps
1. Build Reddit data ingestion pipeline
2. Adapt similarity engine for Reddit content
3. Test on r/programming, r/technology
4. Deploy as moderator tool
5. Gather feedback, iterate

## Hackathon Requirements
- [x] Architecture document
- [x] Data model design
- [x] API integration plan
- [ ] Prototype implementation
