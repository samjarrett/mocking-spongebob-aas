# Mocking Spongebob as a Service (MSaaS)

Will generate a [mocking spongebob](https://knowyourmeme.com/memes/mocking-spongebob) meme on demand. 

## How?

This is deployed to `https://mock.sam.wtf`, and will accept the first path of the URL as the text to mock. Spaces and other characters are allowed, as long as they're URL-encoded (query-string like encoding is allowed, so `+` will translate to a space). 

![Example](https://mock.sam.wtf/an+example+generated+meme)
