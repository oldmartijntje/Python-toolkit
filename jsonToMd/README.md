Getting every matpat video, by pasting the following js into the console:

```js
var scroll = setInterval(function(){ window.scrollBy(0, 2000)}, 2000);
```

And then by waiting for it to scroll down and paste the following code (that I made myself):
```js
window.clearInterval(scroll);console.clear(); urls = $$('a');ii = 0; json = [];urls.forEach(function(v,i,a){if (v.id=="video-title-link"){json.push({"id":ii, "title": v.title, "link": v.href });ii++;}});console.log(json);jsonString = JSON.stringify(json);console.log(jsonString);
```

This will log every link + title in json format.

Then you copy the second message and paste it into a file, and call it name.json

Paste this file into the input/ folder.