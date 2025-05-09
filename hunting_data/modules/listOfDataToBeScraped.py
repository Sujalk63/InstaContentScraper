scrapable_fields = [
    "post_id",
    "post_type",
    "video_duration",
    "aspect_ratio",
    "caption_text",
    "caption_length",
    "hashtag_count",
    "hashtags_used",
    "audio_used",
    "is_trending_audio",
    "thumbnail_present",
    "mentions_count",
    "link_in_caption",
    "posted_time",
    "day_of_week",
    "hour_of_day",
    "is_peak_hour",
    "language_detected",
    "days_since_last_post"
]


postprocessing_fields = [
    "posting_consistency",       # from multiple post dates
    "caption_length",            # computed from text
    "hashtag_count",             # count of hashtags
    "mentions_count",            # count of @mentions
    "link_in_caption",           # check if 'http' in caption
    "day_of_week",               # from posted_time
    "hour_of_day",               # from posted_time
    "is_peak_hour",              # define time range (e.g., 6-10PM)
    "language_detected",         # use langdetect or similar
    "days_since_last_post",      # from datetime diff of post
]

ml_required_fields = [
    "sentiment_score",           # from caption/comments using NLP
    "hook_detected",             # needs first 3s video analysis
    "visual_quality_score",      # from image/video quality models
    "content_type_tag",          # from NLP classification on caption
    "virality_score",            # custom scoring (based on views, likes)
    "viral"                      # define threshold to flag
]



scrapable_fields = [
    # Post Basics
    "post_id",
    "post_type",  # "Reel" or "Post"
    "posted_time",
    "day_of_week",
    "hour_of_day",
    # "is_peak_hour", 

    # Media & Content Info
    "video_duration",
    "aspect_ratio",
    "thumbnail_present",
    "caption_text",
    "caption_length",
    "hashtags_used",
    "hashtag_count",
    "mentions_count",
    "all_mentions",
    "link_in_caption",
    "audio_used",
    "is_trending_audio",

    # Engagement Metrics
    "likes_count",
    "comments_count",
    "views_count",   # Especially useful for Reels
    "saves",         # If visible
    "shares",        # If available — often not public

    # Analysis & Scoring
    "virality_score",      # Calculated later
    "viral",               # Boolean: based on threshold
    "days_since_last_post",
    "posting_consistency", # Avg. days between posts
    "content_type_tag",    # e.g., funny, vlog, motivational
    "sentiment_score",     # NLP-based, from caption/comments
    "visual_quality_score",# Custom heuristic/model-based
    "hook_detected"        # True/False — first 3 sec analysis
]
