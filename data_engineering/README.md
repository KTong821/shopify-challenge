# Shopify Data Engineering Challenge

Hi! This is my data engineering challenge submission.

Cutting to the chase, here are the main features:

* Bulk upload
* Authentication using OAuth 2.0 Device Authorization Flow
* Duplicate checking
* File sync

The idea was to have a remote backup of local files (doesn't have to be images) on AWS S3. Access can be controlled, but for this demo anyone can create an account and access the same repository.

## Instructions 

1. Clone this repo!
2. Go put some images in the data folder. This can be configured, but to keep it simple let's just use this one.
3. We'll need to know where you stored the data. Run `pwd` in this `data_engineering` directory.
4. Hopefully you have docker installed! Run `docker build -t shopify-image-repo .` in this data engineering directory (where the Dockerfile is).
5. Run `docker run --env-file .env -v <PWD_COMMAND_OUTPUT>/data:/usr/data_upload/data -it shopify-image-repo`, substituting `<PWD_COMMAND_OUTPUT>` with what you got in step 2. For example, I get something like `..../shopify-challenge/data_engineering`. This uploads your file to the repo, with some authentication steps given by the command line output.
6. To perform a file sync, run the same command above and tack on `sync` at the end. I've pre-saved some images in the repo for you to check out! (Locally the system caches credentials so you don't have to login twice, but I can't do that in a docker container without a shared volume.)


If anything goes wrong, please feel free to email me at `kevin.tong@uwaterloo.ca`

Sample (but working) tests for the file upload/download function can be found in the tests folder.
## Thing to Improve 

Here are some things I'd improve if I had more time:

* File duplicate checking is done by comparing hashes. These should be stored in a database with partition key being these hash values (instead of a hacky text file)!
* Encapsulation is definitely needed. Some things are global right now, and that's bad practice.
* Throwing in a lambda function or ECS task triggered by new file uploads would be really simple; it could run an image caption transformers model to enable searching by descriptions. Elasticsearch sounds like a good candidate for this.
