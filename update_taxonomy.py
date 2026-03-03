import os
import re

directory = 'content/posts'

category_map = {
    'Technolgic': 'Tech',
    'emacs': 'Tech',
    'Tech': 'Tech',
    'AI': 'AI',
    'Life': 'Life',
    'Algorithm': 'Algorithm',
    'Reading': 'Reading'
}

tag_map = {
    'distribute': 'distributed-system',
    'alg@geeedy': 'greedy',
    'alg@dp': 'dp',
    'alg@backtrack': 'backtracking',
    'alg@simulation': 'simulation',
    'alg@binarySearch': 'binary-search',
    'alg@hash': 'hash-table',
    'alg@arr': 'array',
    'java': 'java',
    'jvm': 'jvm',
    'hugo': 'hugo',
    'AI编程': 'ai-programming',
    '行业思考': 'thoughts',
    '经验分享': 'experience',
    '研发效能': 'productivity'
}

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update categories
        def cat_repl(match):
            cats = match.group(1).replace('"', '').replace(' ', '').split(',')
            new_cats = []
            for c in cats:
                if c in category_map:
                    new_cats.append(category_map[c])
                elif c == 'AI' or c == 'Tech': # Handle arrays like ["Tech", "AI"]
                    new_cats.append(category_map.get(c, c))
                else:
                    new_cats.append(c)
            # Make unique and format
            new_cats = list(set(new_cats))
            
            # Special rule: If AI is present, we make it the primary category and maybe remove Tech if we want AI standalone
            if 'AI' in new_cats:
                new_cats = ['AI'] # As requested: "ai 独立出来做一个 类目"
                
            formatted = ', '.join([f'"{c}"' for c in new_cats])
            return f'categories = [{formatted}]'

        # Update tags
        def tag_repl(match):
            tags = match.group(1).replace('"', '').replace(' ', '').split(',')
            new_tags = []
            for t in tags:
                clean_t = t.strip()
                if clean_t in tag_map:
                    new_tags.append(tag_map[clean_t])
                else:
                    new_tags.append(clean_t)
            formatted = ', '.join([f'"{t}"' for t in set(new_tags) if t])
            return f'tags = [{formatted}]'

        new_content = re.sub(r'categories\s*=\s*\[(.*?)\]', cat_repl, content)
        new_content = re.sub(r'tags\s*=\s*\[(.*?)\]', tag_repl, new_content)
        
        # Add tags to files that don't have them but should (based on category)
        if 'tags =' not in new_content:
            if 'categories = ["Algorithm"]' in new_content:
                new_content = new_content.replace('categories = ["Algorithm"]', 'tags = ["leetcode"]\ncategories = ["Algorithm"]')
            elif 'categories = ["Life"]' in new_content:
                new_content = new_content.replace('categories = ["Life"]', 'tags = ["yearly-review"]\ncategories = ["Life"]')
            elif 'categories = ["Reading"]' in new_content:
                new_content = new_content.replace('categories = ["Reading"]', 'tags = ["book-review"]\ncategories = ["Reading"]')
            elif filename == 'ox-hugo-集成-mermaid.md' or filename == '利用 emacs + hugo 搭建个人博客.md':
                 new_content = new_content.replace('categories = ["Tech"]', 'tags = ["emacs", "hugo"]\ncategories = ["Tech"]')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

print("Taxonomy updated successfully.")