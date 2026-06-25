def calculate_jaccard_similarity(user_interests, item_tags):
    """
    Calculates Jaccard Similarity between user interests and item tags.
    Formula: Size of Intersection / Size of Union
    """
    # Convert lists to sets to ensure exact vocabulary matching
    user_set = set(user_interests)
    item_set = set(item_tags)
    
    # Calculate the size of the intersection (overlapping tags)
    intersection = user_set.intersection(item_set)
    
    # Calculate the size of the union (all unique tags combined)
    union = user_set.union(item_set)
    
    # Prevent division by zero if both sets are empty
    if not union:
        return 0.0
        
    return len(intersection) / len(union)


def get_recommendations(user_profile, item_dataset, top_n=3):
    """
    Processes item dataset against user preferences using similarity logic 
    and outputs a ranked Top-N recommended list.
    """
    recommendation_scores = []
    
    # Standardize user inputs to prevent naming mismatches from breaking the math
    standardized_user_interests = [interest.strip().lower() for interest in user_profile]
    
    for item in item_dataset:
        # Standardize item tags to match the shared vocabulary space
        standardized_item_tags = [tag.strip().lower() for tag in item['tags']]
        
        # Calculate algorithmic match percentage
        score = calculate_jaccard_similarity(standardized_user_interests, standardized_item_tags)
        
        # Store item data along with its calculated score
        recommendation_scores.append({
            'title': item['title'],
            'category': item['category'],
            'tags': item['tags'],
            'score': round(score, 4)
        })
        
    # Sort recommendations based on similarity score in descending order
    ranked_recommendations = sorted(recommendation_scores, key=lambda x: x['score'], reverse=True)
    
    # Return the truncated Top-N results
    return ranked_recommendations[:top_n]


# =====================================================================
# SYSTEM EVALUATION & TEST DATASET
# =====================================================================

# Mock database mapping intrinsic item features
course_catalog = [
    {
        "title": "Python for Data Science",
        "category": "Data Science",
        "tags": ["Python", "Data Analysis", "Pandas", "Automation"]
    },
    {
        "title": "Advanced Neural Networks",
        "category": "Artificial Intelligence",
        "tags": ["Neural Networks", "Tensors", "Optimization", "Python"]
    },
    {
        "title": "Cloud Automation & DevOps",
        "category": "Cloud Computing",
        "tags": ["Cloud", "Automation", "AWS", "Docker"]
    },
    {
        "title": "Frontend Development Foundations",
        "category": "Web Design",
        "tags": ["HTML", "CSS", "JavaScript", "Frontend Development"]
    }
]

if __name__ == "__main__":
    print("-" * 50)
    print("      DECODELABS AI RECOMMENDATION ENGINE v1.8    ")
    print("-" * 50)
    
    # Step 1: Simulate Input (Explicit choices)
    print("\n[INPUT] Simulating user profile tag collection...")
    # NOTE: Exact vocabulary mapping is vital. Discrepancies break the match logic.
    user_interests = ["Python", "Neural Networks", "Optimization"]
    print(f"Captured User Interests: {user_interests}")
    
    # Step 2: Process (Pattern Matching using Jaccard Similarity Math)
    print("\n[PROCESS] Comparing vector overlap against item catalog...")
    top_suggestions = get_recommendations(user_profile=user_interests, item_dataset=course_catalog, top_n=2)
    
    # Step 3: Output (Display Recommended Items)
    print("\n[OUTPUT] Final Top-N Tailored Recommendation List:")
    print("=" * 50)
    for index, item in enumerate(top_suggestions, 1):
        match_percentage = item['score'] * 100
        print(f"{index}. Title: {item['title']}")
        print(f"   Category: {item['category']}")
        print(f"   Tags: {item['tags']}")
        print(f"   Algorithmic Confidence: {match_percentage:.2f}% Match")
        print("-" * 50)