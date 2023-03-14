# Task 5: Authority Finding in Twitter

In this task, the participating systems are required to retrieve a set of authority Twitter accounts for a given rumor propagating in Twitter. Given a tweet stating a rumor, a model has to retrieve a _ranked list_ of authority Twitter accounts that can help verify the rumor; i.e. they may tweet evidence that supports or denies the rumor. This task is offered in _Arabic_.

<!-- ## Data-sharing Agreement


**Data is available at** -->

__Table of Content:__

- [List of Versions](#list-of-versions)
- [Contents of Task 5 Directory](#contents-of-task-5-directory)
- [Input Data Format](#input-data-format)
- [Output Data Format](#output-data-format)
- [Evaluation Metrics](#evaluation-metrics)
- [Baselines](#baselines)
- [Recommended Reading](#recommended-reading)
- [Resources and Tools](#resources-and-tools)
- [Task Organizers](#task-organizers)
- [Credits](#credits)


# List of Versions
- **Task 5--Arabic-v1.0 [2023/01/19]** - Data for Task 5 is released. 

# Content of Task 5 Directory
We provide the following:
* Main folder: [data](./data)
  * Subfolder: [subtask-5A-arabic](./data/subtask-5A-arabic)
  	This directory contains files for the authority finding task offered in Arabic.    
  __Note__: Users metadata can be downloaded from [here](https://drive.google.com/drive/folders/1AzCwNq1IukK1Sm9je_SupDTauL-STYk4?usp=sharing). 	

<!-- * Main folder: [baselines](./baselines)<br/>
	Contains scripts provided for baseline models of the tasks. -->

# Input Data Format

## Rumors

We provide train and dev splits in JSON format. Each split file has a list of JSON objects representing rumors. For each rumor, we provide the following entries:
```
{
  rumor_id [unique ID for the rumor]
  tweet_id [unique tweet ID as provided by Twitter]
  tweet_text [tweet text as collected from Twitter]
  category [category of the rumor which is either politics, sports, or health]
}
```
Examples:

```
{
  "rumor_id": "AuFIN_024",
  "tweet_id": 1355061889122889729,
  "tweet_text": "خبر سار لجماهير الاهلي.. بي ان سبورت تختار احمد الطيب للتعليق علي مباراة الاهلي والدحيل ف افتتاح كاس العالم للاندية https://t.co/JPNHMcNyZM",
  "category": "sports"
},
...,
{
  "rumor_id": "AuFIN_034",
  "tweet_id": 1329019940435849217,
  "tweet_text": "بعد تعينه نائب رئيس الجمعية الدستورية القطرية الرئيس قيس سعيد يقسم اليمين امام صاحبة السمو الشيخة موزة المسند فى عاصمة #قطر الدوحة https://t.co/kCYFDQHYcS",
  "category": "politics"
},
...

```

## Relevance Judgments (Qrels)

It is a TAB-separated file in [TREC](https://trec.nist.gov/) format. Each rumor ID is associated with user IDs of the authorities. The file is in the following format
> rumor_id <TAB> 0 <TAB> user_id <TAB> relevance

where: <br/>
* rumor_id: Unique ID for the given rumor
* 0: Literally 0 (this column is needed to comply with the TREC format)
* user_id: Unique ID for the given authority
* relevance: 2 if the authority is _highly relevant_ to the rumor (has higher priority to be contacted); 1 if she is _relevant_

__Note__: In the qrels file, only pairs with relevance = 1 or 2 are reported. Relevance = 0 is assumed for all pairs not appearing in the qrels file.

Example:

| rumor_id | 0 | user_id | relevance |
|---|---|---|---|
| AuFIN_042 | 0 | 129518457  |  2 |
| AuFIN_042 | 0 | 45522292 |  2 |
| AuFIN_042 | 0 | 722486044059398144 | 1 |
| AuFIN_042 | 0 | 745198763552145409 | 1 |
| AuFIN_042 | 0 | 43580047 | 1 |
| AuFIN_013 | 0 | 259372802 | 1 |
| AuFIN_013 | 0 | 931668301 | 1 |
| AuFIN_013 | 0 | 745581936421257216 | 2 |
|... |

## Users Metadata

We provide [a collection of 1000 JSON files with users information](https://drive.google.com/drive/folders/1FQORc039HauQvlXORTr-MQI1EAlpDVAT?usp=sharing). Each file has a list of JSON objects representing users. For each user we provide the following entries: 
```
{
  user_id [the unique user ID as provided by Twitter]
  name [the name of the user, as they’ve defined it on their profile]
  description [the text of this user's profile description (also known as bio), if the user provided one]
  translated_name [the name of the user translated by us into Arabic]
  translated_desc [the user's profile description translated by us into Arabic]
  following_count [the number of Twitter users this user is following]
  followers_count [the number of Twitter users following this user]
  verified [indicates if this user is a verified Twitter User (1 or 0)]
  lists_count [the number of Twitter lists this user is member of]
  lists_ids [list of unique IDs of the Twitter lists the user is member of if exists]
  collected_Arabic_tweets_ids [unique IDs of Arabic tweets posted by this user (recent at the collection time)]  
}
```
Example:

```
{
  "user_id": 1303766076,
  "name": "UNDPIraq",
  "description": "Committed to supporting the people & Government of Iraq during the transition towards reconciliation, reform & stability.",
  "translated_name": "برنامج الأمم المتحدة الإنمائي العراق",
  "translated_desc": "ملتزمون بدعم حكومة الشعب العراقي خلال فترة الانتقال نحو المصالحة الإصلاحية والاستقرار",
  "following_count": 295,
  "followers_count": 21814,
  "verified": 1,
  "lists_count": 196,
  "lists_ids": "1441652508531646465,1438861026968092672,1437411195066142729,........
  "collected_Arabic_tweets_ids": "1425811783835557897,1401106018323599363,1313790186816446464,...
}
```
## Twitter Lists Metadata

We provide a collection of 1000 JSON files with Twitter lists information. Each file has a list of JSON objects representing Twitter lists. For each Twitter list, we provide the following entries: 
```
{
  list_id [the unique list ID as provided by Twitter]
  name [the name of the list, as defined when creating the list]
  description [a brief description to let users know about the list, if the user provided one]
  translated_name [the name of the list translated by us into Arabic]
  translated_desc [the list's description translated by us into Arabic]
  member_count [the number of users that are part of this list (added as members by the owner)]
  follower_count [the number of users following this list]
  created_at [the UTC datetime that the list was created on Twitter]
  owner_id [unique ID of the user who owns (created) this list]
  owner_name [the name of the user who owns (created) this list, as they’ve defined it on their profile]
}
```
Example:

```
{
  "list_id": 61845497,
  "name": "Tech News",
  "description": "Talking about the latest technological inventions and events.",
  "translated_name": "أخبار التكنولوجيا",
  "translated_desc": "الحديث عن أحدث الاختراعات والأحداث التكنولوجية",
  "member_count": 13,
  "follower_count": 2,
  "created_at": "Wed Dec 28 19:43:53 +0000 2011",
  "owner_id": 180411223,
  "owner_name": "𝙷𝚊𝚒𝚍𝚊𝚛 𝚉𝚎𝚒𝚗𝚎𝚍𝚍𝚒𝚗𝚎"
},
```
# Output Data Format

Each row of the result file is related to a pair (rumor_id, user_id) and intuitively indicates the ranking of the authorities with respect to the input rumor.
Each row should be in the following format:

> rumor_id <TAB> Q0 <TAB> user_id <TAB> rank <TAB> score <TAB> tag

where <br/>
* rumor_id: The unique ID for the given rumor
* Q0: This column is needed to comply with the TREC format
* user_id: The unique ID for the user (authority) for the given rumor as found in the users metadata
* rank: the rank of the user for that given rumor_id
* score: the score given by your model for the user given the rumor
* tag: the string identifier of the team/model

# Evaluation Metrics

The task is evaluated as a ranking task. The official evaluation measure is P@5 to evaluate how systems are able to retrieve authorities at the top of a short retrieved list. Other measures, such as P@1 and nDCG@5, will also be reported.

# Baselines

TBA

<!-- ## Scorers -->
# Recommended Reading

The following papers might be useful for the task. We have not provided an exhaustive list, but this could be a good start.

* Liang, C., Liu, Z., Sun, M., 2012. Expert finding for microblog misinformation identification, in: Proceedings of COLING 2012: Posters, pp.703–712.
* Li, G., Dong, M., Yang, F., Zeng, J., Yuan, J., Jin, C., Hung, N.Q.V., Cong, P.T., Zheng, B., 2020. Misinformation-oriented expert finding in social networks. World Wide Web 23, 693–714.
* Ghosh, S., Sharma, N., Benevenuto, F., Ganguly, N., Gummadi, K., 2012. Cognos: Crowdsourcing Search for Topic Experts in Microblogs, in: Proceedings of the 35th International ACM SIGIR Conference on Research and Development in Information Retrieval, Association for Computing Machinery, New York, NY, USA. p. 575–590. 
* Ma, Y., Yuan, Y., Wang, G., Wang, Y., Ma, D., Cui, P., 2019. Local experts finding across multiple social networks, in: International Conference on Database Systems for Advanced Applications, Springer. pp. 536–554
* Lahoti, P., De Francisci Morales, G., Gionis, A., 2017. Finding topical experts in Twitter via query-dependent personalized PageRank, in: Proceedings of the 2017 IEEE/ACM International Conference on Advances in Social Networks Analysis and Mining 2017, pp. 155–162.

# Resources and Tools
We suggest the following resources/tools, which might be helpful to implement your models.

* [Pyserini](https://github.com/castorini/pyserini): a Python toolkit for information retrieval research 
* [Pyterrier](https://github.com/terrier-org/pyterrier): a Python toolkit for information retrieval research 
* [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools): a suite of Arabic natural language processing tools. 
* [PyArabic](https://pypi.org/project/PyArabic/): A specific Arabic language library for Python, provides basic functions to manipulate Arabic letters and text.

# Task Organizers
- [Tamer Elsayed](http://qufaculty.qu.edu.qa/telsayed/) (Qatar University)
- [Fatima Haouari](https://sites.google.com/view/bigir/members/fatima-haouari) (Qatar University)

# Credits
Please find it on the task website: https://checkthat.gitlab.io/clef2023/task5/
