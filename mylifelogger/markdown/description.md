<!--
This file supports markdown formatting.
Use markdown to format the text. This markdown gets parsed into html when sending email.

More information about markdown formatting:
https://guides.github.com/features/mastering-markdown/

Available variables(data inputted by you are available as variables):
title => Title for the event
date_created => Date of occurence of event
short_description
time_since => Time since event occurance

Variables can be used with this syntax =>
{{ var_name }}
-->

**Time since event** : {{time_since}}

# Vimeo Downloader

  

Download Vimeo videos and retrieve metadata such as views, likes, comments, duration.

  

* Easy to use and friendly API.

* Support for downloading private and embed Vimeo videos.

* Retrieve direct URL for the video file.

* Tested on Python and 3.6, 3.7, 3.8, 3.9

  
  

## Installation

  

```bash

pip install vimeo_downloader

```

  

## Usage

  

```python

>>> from vimeo_downloader import Vimeo

>>> v = Vimeo('https://vimeo.com/503166067')

>>> meta = v.metadata

>>> meta.title

"We Don't Have To Know - Keli Holiday"

>>> meta.likes

214

>>> meta.views

8039

>>> meta._fields # List of all meta data fields

('id', 'title', 'description'...) # Truncated for readability

>>> s = v.streams

>>> s

[Stream(240p), Stream(360p), Stream(540p), Stream(720p), Stream(1080p)]

>>> best_stream = s[-1] # Select the best stream

>>> best_stream.filesize

'166.589421 MB'

>>> best_stream._direct_url
'https://vod-progressive.../2298326263.mp4'

  
  

```

  

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

  

Please make sure to update tests as appropriate.

  

## License

[MIT](https://choosealicense.com/licenses/mit/)
