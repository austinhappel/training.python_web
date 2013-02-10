<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Administer posts</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <a href="new_post">Create a new post</a>
    <h1>All Posts:</h1>
    <ul>
        %for post in posts:
            <li><a href="/post/{{ post.id }}">{{ post.title }}</a></li>
        %end
    </ul>
</body>
</html>