<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>published on: {{ post.publish_date }}</p>
    <div class="content">
        {{ post.content }}
    </div>
</body>
</html>