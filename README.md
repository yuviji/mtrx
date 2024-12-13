# mtrx — /ˈmɛtrɪks/
### Data analytics solutions for small businesses.
Team: Wyatt Lake, Sritan Motati, Yuvraj Lakhotia, Evelyn Li

## Components
- Client Portal: https://github.com/wyattlake/penn-apps-frontend
- LLM & API Suite: https://github.com/sritanmotati/pennapps-backend
- CORS Server: https://github.com/sritanmotati/cors-server
- Web Scraper: https://github.com/yuviji/mtrx-scraper
- Video Demo: https://www.youtube.com/watch?v=5DYp92nrwiw

## Inspiration
As first-years who recently moved onto Penn’s city campus, we’ve explored many new restaurants, and grown to appreciate the variety of family-owned dining spots. We wanted to create an accessible application that helps small businesses track their analytics against other similar companies and develop a deeper understanding of their potential action points. Our product inspiration stemmed from existing softwares such as Revinate, which creates complex and actionable insights from tons of messy data for large corporations such as hotels. With mtrx, we’re bringing this utility to the companies that really need it.

## What it does
mtrx provides AI-enhanced actionable metrics for small businesses that don’t have the infrastructure to compute these statistics. It scrapes data from Yelp and processes it using our LLM suite to understand the business's current situation and suggest improvements.

## How we built it
mtrx is composed of a three-part solution. The [portal](https://github.com/wyattlake/penn-apps-frontend), [API](https://github.com/sritanmotati/pennapps-backend), and [scraper](https://github.com/yuviji/mtrx-scraper).

**1. Client Portal ([Svelte](https://svelte.dev/)):** The web interface that small businesses can easily access, sign up for, and view metrics from. The portal uses [ApexCharts](https://www.npmjs.com/package/svelte-apexcharts) for visualizing our data and metrics, [Firebase](https://firebase.google.com/) for authentication and account information, and [Flowbite](https://flowbite.com/) for broader UI components. We implemented a cross-origin resource sharing (CORS) proxy-server that allowed us to access our REST API on Ploomber, and designed the visuals with [Adobe XD](https://adobexdplatform.com/).

**2. LLM & API Suite ([Python](https://www.python.org/)):** We performed large-scale sentiment analysis on review data for many businesses. This was done with the [DistilBERT](https://huggingface.co/docs/transformers/en/model_doc/distilbert) architecture provided through Hugging Face, which performed at a state-of-the-art level. For the rest of our LLM needs, which were used to analyze the content of reviews and generate suggestions for an improved business strategy, we used [Cerebras](https://cerebras.ai/)
 and [Tune Studio](https://tunehq.ai/tune-studio). The base Llama models were accessed with Cerebras for lightning-fast inference, and Tune Studio served as a convenient wrapper/pipeline to access the Cerebras models.

All of our AI-based functionalities and asynchronous scraping scripts were implemented within a custom REST API developed with [Flask](https://flask.palletsprojects.com/en/3.0.x/). To deploy and host our API, we tested many free solutions, but most did not provide enough compute to support transformer-based sentiment analysis. After unsuccessfully trying out [Railway](https://railway.app/), [Vercel](https://vercel.com/), [Render](https://render.com/), and [AWS EC2](https://aws.amazon.com/ec2/), we ended up using [Ploomber](https://ploomber.io/), a Y-Combinator W22 startup offering Heroku-like services for AI projects.

**3. Web Scraper ([Python](https://www.python.org/)):** Initially, we built a foundational database by scraping [Yelp](https://www.yelp.com/) for restaurants in our area (Philadelphia) using a custom [Selenium](https://www.selenium.dev/) web scraper that posted the data to Firebase, from where it processed and analyzed by the LLM suite. We later developed an asynchronous web scraper than can gather data on a business __*as they sign up*__ for mtrx using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and embedding it directly into a REST API call/route — enabling access to mtrx for nearly any client that wishes to use it.

## Challenges we ran into
The ride was most definitely not smooth.

Finding a cloud hosting platform whose free-tier met our CPU and memory requirements for the Flask server was difficult – we tried Vercel, Railway, AWS, etc. – and ultimately decided on Ploomber, which provided us with 1 vCPU and 2 GiB RAM.

We couldn’t send requests from our local web interface to the Ploomber REST API server that we had deployed – the problem was that the web app itself wouldn’t issue any requests unless we had a cross-origin resource sharing (CORS) server configured. It took a while to set up, but after setup, we could send and receive information from our Flask backend!

The Ploomber server also had a timeout period for requests, which meant that we had to optimize our asynchronous scraping and analysis processes in order to prevent time-outs and server errors. As a result, the amount of data available dynamically is not at its fullest potential.

## Accomplishments that we're proud of
This project was a great learning experience for all of us. We got to learn a lot about front-end and back-end development. Through exploring many different REST APIs and our sponsor’s products, we compiled an LLM & API Suite with enough memory to perform our Natural-Language-Processing tasks. Overall, it was rewarding for our team to be able to turn an idea into a product — and accomplish all of our planned tasks!

## What we learned
We learned how to efficiently conduct a division of tasks, product management, and integrate various technologies into one application. We also got to implement sentiment analysis and LLMs. We also gained hands-on experience in developing Flask backends and creating responsive front-end designs with CSS, enhancing our full-stack development skills.

## What's next for mtrx
We plan on sourcing customer reviews from diverse platforms, reaching out to local small businesses to provide demos, and offering pro-bono services to local businesses. By expanding our dataset and testing our product in the real-world, we’ll be able to improve our product more efficiently and cater to our projected audiences.
