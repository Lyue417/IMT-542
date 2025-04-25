import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import os

def load_data(json_path):
    """Load the integrated director data from JSON file"""
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find file at {json_path}")
        print("Please make sure the file exists or specify the correct path using --data")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File at {json_path} is not a valid JSON file")
        sys.exit(1)

def analyze_directors(data, top_n=15):
    """Analyze top directors by number of movies"""
    # Create a list of directors with their stats
    directors_list = []
    
    for director, info in data.items():
        if info["count_in_top1000"] > 0:
            directors_list.append({
                "name": director,
                "count": info["count_in_top1000"],
                "avg_rating": info["avg_rating_top1000"]
            })
    
    # Sort by count of movies
    directors_list.sort(key=lambda x: x["count"], reverse=True)
    
    # Return the top N directors
    return directors_list[:top_n]

def analyze_decades(data, director_name):
    """Analyze a director's performance by decade"""
    if director_name not in data:
        print(f"Director {director_name} not found in data")
        return None
    
    director_data = data[director_name]
    decades = director_data["decades"]
    
    decades_data = []
    for decade, info in decades.items():
        if decade != "unknown" and int(decade) > 0:
            decades_data.append({
                "decade": decade,
                "count": info["count"],
                "avg_rating": info["avg_rating"] if "avg_rating" in info else 0
            })
    
    # Sort by decade
    decades_data.sort(key=lambda x: int(x["decade"]))
    return decades_data

def visualize_top_directors(directors_data, output_path=None):
    """Create a bar chart of top directors by movie count"""
    names = [d["name"] for d in directors_data]
    counts = [d["count"] for d in directors_data]
    ratings = [d["avg_rating"] for d in directors_data]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(names, counts, color='skyblue', alpha=0.7)
    
    # Add rating labels above bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'Rating: {ratings[i]:.1f}', ha='center', va='bottom', 
                rotation=0, fontsize=9)
    
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.title('Top Directors by Number of Movies in IMDB Top 1000', fontsize=14)
    plt.ylabel('Number of Movies', fontsize=12)
    plt.tight_layout()
    
    if output_path:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    
    plt.show()

def visualize_director_decades(decades_data, director_name, output_path=None):
    """Create a visualization of a director's performance by decade"""
    if not decades_data:
        return
        
    decades = [d["decade"] for d in decades_data]
    counts = [d["count"] for d in decades_data]
    ratings = [d["avg_rating"] for d in decades_data]
    
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    # Plot bar chart for movie counts
    color = 'tab:blue'
    ax1.set_xlabel('Decade', fontsize=12)
    ax1.set_ylabel('Number of Movies', fontsize=12, color=color)
    bars = ax1.bar(decades, counts, color=color, alpha=0.7)
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Add a second y-axis for ratings
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Average Rating', fontsize=12, color=color)
    ax2.plot(decades, ratings, color=color, marker='o', linestyle='-', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)
    
    plt.title(f'{director_name}: Movies and Ratings by Decade', fontsize=14)
    plt.tight_layout()
    
    if output_path:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        print(f"Visualization saved to {output_path}")
    
    plt.show()

def main():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Analyze IMDB director data')
    parser.add_argument('--data', type=str, default='data/integrated_directors.json',
                        help='Path to the integrated directors JSON file')
    parser.add_argument('--director', type=str, 
                        help='Name of a specific director to analyze by decade')
    parser.add_argument('--top_n', type=int, default=15, 
                        help='Number of top directors to display')
    parser.add_argument('--output_dir', type=str, default='examples',
                        help='Directory to save output visualizations')
    
    args = parser.parse_args()
    
    # 使用脚本所在目录处理相对路径
    if not os.path.isabs(args.data):
        args.data = os.path.join(script_dir, args.data)
        
    if args.output_dir and not os.path.isabs(args.output_dir):
        args.output_dir = os.path.join(script_dir, args.output_dir)
    
    # Load data
    print(f"Loading data from {args.data}...")
    data = load_data(args.data)
    print("Data loaded successfully!")
    
    # Analyze and visualize top directors
    print(f"Analyzing top {args.top_n} directors...")
    top_directors = analyze_directors(data, args.top_n)
    
    output_path = None
    if args.output_dir:
        output_path = os.path.join(args.output_dir, 'top_directors.png')
    
    visualize_top_directors(top_directors, output_path)
    
    # If a specific director is provided, analyze their decades
    if args.director:
        print(f"Analyzing {args.director}'s career by decade...")
        decades_data = analyze_decades(data, args.director)
        
        if decades_data:
            decade_output_path = None
            if args.output_dir:
                # Create a valid filename from the director name
                safe_name = args.director.replace(" ", "_").replace("/", "_")
                decade_output_path = os.path.join(args.output_dir, f'{safe_name}_decades.png')
            
            visualize_director_decades(decades_data, args.director, decade_output_path)
        else:
            print(f"No decade data available for {args.director}")

if __name__ == "__main__":
    main()