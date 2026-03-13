# Fashion Finder (Name WIP)
This is a new project that aims to let users find an assortment of clothes in their price range that are similar to ones they wear or are just interested in. Hopefully, this can be used so that people don't have to break the bank to maintain their style.


## Tech Stack

### ML:
- CLIP (OpenClip)
- Python (PyTorch)
- NumPy, Pandas

### Backend/API/Database:
- FastAPI hosted on 
- Postgres + pgvector hosted on Amazon RDS
- Amazon S3

### Frontend/UI:
- Next.js
- Tailwind or ChakraUI


## Setup

### __Before Getting Started__: Ensure that your machine has <ins>Python 3.9+</ins> installed.

### Clone the repository
```
git clone https://github.com/tentsundue/fashion-finder.git
cd fashion-finder
```

### Setup the virtual environment (venv)

Windows:
```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```
Note that this would install the CPU version of pytorch if on Windows. 

If you have a GPU and would prefer to use that, then see _https://pytorch.org/get-started/locally/_

Whichever is downloaded doesn't seem to matter much at the moment (because the project is still early WIP)
but it's worth mentioning that `clip_model.py` prioritizes the GPU version if installed, defaulting to CPU if not.


### Download Images from `metadata.csv`

#### Context:
I am currently doing this in my web scraper, which is located in another repository, linked in the `References` section below. It builds the metadata for each product across a select portion of clothing vendors and downloads the appropriate images. The folder strucutre is organized a bit differently than how it is in this repo so the script for downloading is not one-to-one at the moment. I will move the script over to this repo once it is refactored. 

#### The Important Part:
You will have to clone the _Clothing Website Scraper_ repo, set it up, run the `download_images.py` script, and manually move the downloaded images into `data/images/{vendor_name}.

It's just a matter of moving folders but could still take around 5 min depending on how many vendors I have at that moment. As of `Feb 6, 2026`, it's just Uniqlo products.


### Configure AWS
The application uses Boto3, python's AWS SDK, to interact with the AWS services used like Amazon S3. To use it, you'll have to configure your AWS credentials. 

Ensure you have an IAM account set up and the [AWS CLI](https://aws.amazon.com/cli/) installed before continuing. Once you do, run:
```
aws configure
```

Input your credentials and AWS region when asked:
```
aws_access_key_id = [YOUR_ACCESS_KEY]
aws_secret_access_key = [YOUR_SECRET_KEY]
Default region name [None]=us-east-1
Default output format [None]: json
```


## References
Clothing Website Scraper, Tenzin Tsundue - https://github.com/tentsundue/clothing-sites-scraper

OpenCLIP GitHub Repository, mlfoundations - https://github.com/mlfoundations/open_clip

AWS SDK for Python (Boto3), AWS - https://aws.amazon.com/sdk-for-python/

FastAPI Documentation, FastAPI
 - [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/#include-an-apirouter-with-a-custom-prefix-tags-responses-and-dependencies)

 - [FastAPI Class](https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI--example)
 
 - [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/#examples-in-json-schema-openapi) 