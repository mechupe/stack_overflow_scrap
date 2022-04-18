# Stack Overflow Questions Dataset
> DataScrappers team datathon results
---

Following repository contains Data Set collected from Stack Overflow  (https://stackoverflow.com/)
and script used for data collection.

## Inspiration

* How popular are some topics on Stack Overflow?
* What popular topics have low answers per questions ratio?
* What python libraries have high accepted answers per questions ratio?
This information might help to decide between several libs with same functionality.

## Script usage

Generate csv files for selected tags:
```bash
python3 main.py --tags python powerquery c++ r keras beautifulsoup
```

Generate csv files for all tags from first 5 tags pages (https://stackoverflow.com/tags):
```bash
python3 main.py --tags_pages 5
```

Generate csv files for all tags from first 5 tags pages (https://stackoverflow.com/tags).
Parse 50 question pages for every tags (there is 50 questions per page):
```bash
python3 main.py --tags_pages 5 --questions_pages 50
```

## Data description

[Data folder](./data)

Collected data stored in .csv format.
Each csv file contains information about one tag, which matches file name.
Values are split by ':' delimiter.

Source example: https://stackoverflow.com/questions/tagged/python?tab=newest&page=5&pagesize=50

**Record example:**

![Question Example](https://github.com/Data-Scrappers/stack_overflow_scrap/blob/main/doc_images/question_example.png)

|   | tag           | id      | vote   | answer | views  | accepted |
|---|---------------|---------|--------|--------|--------|----------|
|6  |beautifulsoup  |23377533 |109     |5       | 197000 |True      |

* **tag** - name of tag;
* **id** - question id. Id is unique for csv file;
* **vote** - number of votes - how the community indicates which questions and answers are most useful and appropriate;
* **answer** - how many answers;
* **views** - how many users saw the question;
* **accepted** - indicates if question has accepted answer or not;
* **date** - date when question was created in format yyyy-mm-dd.

**Dataframe example:**

![Dataframe example](https://github.com/Data-Scrappers/stack_overflow_scrap/blob/main/doc_images/table_example.png)

**Additional tool: Tags labelling**

If you need to generate csv file with additional information about every tag,
you can launch `label_tags.py` script:

```bash
python3 label_tags.py --path '../data/' --tags 'labelled_tags.csv'
```

``label_tool/labelled_tags.csv`` file contains all tags, where 
* programming language related tags labelled with ``language``
* python modules related tags labelled with ``python-lib``

