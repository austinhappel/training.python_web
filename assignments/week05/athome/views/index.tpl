<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <h1>All Posts</h1>
    %for post in posts:
        <div class="post">
            <h1><a href="/post/{{ post.id }}">{{ post.title }}</a></h1>
            <div>{{ post.content }}</div>
        </div>
    %end
</body>
</html>