# A C/C++ Code Vulnerability Dataset with Code Changes and CVE Summaries

## 1 . Data Description

- CVE entries in our dataset cover the period from 2002 to 2019, each consisting of 21 features. Each feature's name and corresponding column name in the CSV file are explained in the following table. The dataset is released as comma-separated values(CSV) format ([all_c_cpp_release2.0.csv](https://github.com/ZeoVan/MSR_20_Code_Vulnerability_CSV_Dataset/blob/master/all_c_cpp_release2.0.csv)).

|           Features           |    Column Name in the CSV     |                         Description                          |
| :--------------------------: | :---------------------------: | :----------------------------------------------------------: |
|      Access Complexity       |      access\_complexity       | Reflects the complexity of the attack required to exploit the software feature misuse vulnerability |
|   Authentication Required    |   authentication\_required    |  If authentication is required to exploit the vulnerability  |
|     Availability Impact      |     availability\_impact      | Measures the potential impact to availability of a successfully exploited misuse vulnerability |
|          Commit ID           |          commit\_id           |   Commit ID in code repository, indicating a mini-version    |
|        Commit Message        |        commit\_message        |                Commit message from developer                 |
|    Confidentiality Impact    |    confidentiality\_impact    | Measures the potential impact on confidentiality of a successfully exploited misuse vulnerability |
|            CWE ID            |            cwe\_id            |                Common Weakness Enumeration ID                |
|            CVE ID            |            cve\_id            |           Common Vulnerabilities and Exposures ID            |
|           CVE Page           |           cve\_page           |            CVE Details web page link for that CVE            |
|         CVE Summary          |            summary            |                   CVE summary information                    |
|          CVSS Score          |             score             |    The relative severity of software flaw vulnerabilities    |
|        Files Changed         |        files\_changed         |       All the changed files and corresponding patches        |
|       Integrity Impact       |       integrity\_impact       | Measures the potential impact to integrity of a successfully exploited misuse vulnerability\ |
|    Mini-version After Fix    |      version\_after\_fix      |                Mini-version ID after the fix                 |
|   Mini-version Before Fix    |     version\_before\_fix      |                Mini-version ID before the fix                |
|     Programming Language     |             lang              |                 Project programming language                 |
|           Project            |            project            |                         Project name                         |
|         Publish Date         |         publish\_date         |                   Publish date of the CVE                    |
|        Reference Link        |           ref\_ink            |                Reference link in the CVE page                |
|         Update Date          |         update\_date          |                    Update date of the CVE                    |
| Vulnerability Classification | vulnerability\_classification |                      Vulnerability type                      |

- We used the code changes information(minned from commited version patches) to localize which lines of code in the files were modified. Taking modified lines between the two mini-versions as flaw lines, we split the functions in the modified files into vulnerable functions (if there were flaw lines modified in the function) and non-vulnerable functions.

- ~~The cleaned version of split functions is coming soon.~~

- The cleaned version of split functions(CSV format) can be found at: https://drive.google.com/file/d/1-0VhnHBp9IGh90s2wCNjeCMuy70HPl8X/view?usp=sharing  

  

  Some of the intermediary files in the data collecting and cleaning process can be found at:https://drive.google.com/file/d/1E95oVDSO0CfAAs-Q0yav2HBGLZQce_v2/view?usp=sharing
  
  
  
  Pandas is recommended (Python Package, like `pandas.read_csv("filepath/file.csv")` ) to work on the dataset.
  
  
  
  Also JSON format dataset can be found at: https://drive.google.com/file/d/1deNsPfeh77h1SHjJURYOeyCR96JgxB_A/view?usp=sharing
  
  - Split functions are released as comma-separated values(CSV) format:
  
  | Column Name in the CSV |                         Description                          |
  | :--------------------: | :----------------------------------------------------------: |
  |      func_before       | The function before the vulnerability being fixed(if "vul" labeled as "1", then this is the vulnerable function) |
  |       func_after       |       The function after the vulnerability being fixed       |
  |      lines_before      | The modified lines in the founction before the vulnerability being fixed |
  |      lines_after       | The modified lines in the founction after the vulnerability being fixed |
  |          vul           | "1" means vulnerable function and "0" means non-vulnerable function |
  |   vul_func_with_fix    |  The code comments showing how the vulnerability was fixed   |
## 2. HOW To Use The Scripts

- Pre-Requirements
    - [Python3](https://www.linuxbabe.com/ubuntu/install-python-3-6-ubuntu-16-04-16-10-17-04)
  - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
    - [Pandas](https://pandas.pydata.org/getting_started.html)
  
  - How to use
    - First use [scrape_all_the_cve.py](https://github.com/ZeoVan/MSR_20_Code_Vulnerability_CSV_Dataset/blob/master/scripts/scrape_all_the_cve.py) to scrape all the CVE entries on CVE Details
    - Then use [get_commit_info](https://github.com/ZeoVan/MSR_20_Code_Vulnerability_CSV_Dataset/blob/master/scripts/get_commit_info.py) to get commit messages
    - Finally crawl down all the source files and patch files using commit messages above, and then split all the functions in the modified files, see [all_cpp_c_project_with_chrome_android.ipynb](https://github.com/ZeoVan/MSR_20_Code_Vulnerability_CSV_Dataset/blob/master/notebooks/all_cpp_c_project_with_chrome_android.ipynb) for details.
  
  ## Citation
  
  ACM Reference Format:
  
  Jiahao Fan, Yi Li, Shaohua Wang and Tien N. Nguyen. 2020. A C/C++ Code Vulnerability Dataset with Code Changes and CVE Summaries. In MSR ’20: The 17th International Conference on Mining Software Repositories,May 25–26, 2020, MSR, Seoul, South Korea. ACM, New York, NY, USA, 5 pages. https://doi.org/10.1145/3379597.3387501
