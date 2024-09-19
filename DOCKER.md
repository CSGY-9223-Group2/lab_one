## Using Docker

A docker file has been provided in the base folder.

You can use the following commands to build the image and run the container:

```bash
docker build -t pastebin_app .
docker run -d -p 5000:5000 --name pastebin_container pastebin_app
```