#coding=utf8
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import ssl
import pandas as pd
import traceback

ssl._create_default_https_context = ssl._create_unverified_context

# exceptions: 404 not found , 429 too many requests, others

# commit page to diff page
# return diff page link
def commit_to_diff(codeLink):
    try:
        codeSoup=BeautifulSoup(urlopen(Request(codeLink,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        #meta data div
        codeDiv = codeSoup.find('div', class_='u-monospace Metadata')
        for span in codeDiv.findAll('span'):
            a = span.find('a')
            if span.get_text() == "[diff]":
                diffLinks = "https://android.googlesource.com"+a['href']
        return diffLinks
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return commit_to_diff(codeLink)
        if e.code == 404:
            print("\n not found:" + codeLink+ "！")
            return ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("reason", e)
        print("\n skip commit_to_diff:"+codeLink + "！")
        return ""

#get whole project "before" and "after" the commit
def diff_to_project(diffLink):
    try:
        projectSoup=BeautifulSoup(urlopen(Request(diffLink,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        #meta data div
        codeDiv = projectSoup.find('div', class_='u-monospace Metadata')
        for th in codeDiv.findAll('th'):
            #project before
            if th.get_text() == "tree":
                #get sibling
                tree = th.next_sibling
                treeA = tree.find('a')
                treeLink = "https://android.googlesource.com"+treeA['href']
            #project after
            if th.get_text() == "parent":
                #get sibling
                parent = th.next_sibling
                parentA = parent.find('a')
                parentLink = "https://android.googlesource.com"+parentA['href']+"/"
        return treeLink, parentLink
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return diff_to_project(diffLink)
        if e.code == 404:
            print("\n not found:" + diffLink+ "！")
            return "", ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("reason", e)
        print("\n skip diff_to_project:"+diffLink+ "！")
        return "", ""

# get whole file "before" and "after" the commit
# more than one file sometimes
# write two files


def diff_to_file(diffLinks,path):
    try:
        before = []
        projectSoup=BeautifulSoup(urlopen(Request(diffLinks,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        # more than one sometimes
        diffDivs = projectSoup.findAll('pre', class_='u-pre u-monospace Diff')
        for diffDiv in diffDivs:
            files = diffDiv.findAll('a',href=True)
            for file in files:
                fileLink = "https://android.googlesource.com"+file['href']
                before.append(fileLink)
                # the first file?
                first_char = file.get_text()[0]
                print(first_char)
                if first_char == "a":
                    text = ""
                    fileSoup=BeautifulSoup(urlopen(Request(fileLink,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
                    fileContents = fileSoup.find('table', class_='FileContents')
                    if not fileContents:
                        continue
                    fileLines = fileContents.findAll('td', class_='FileContents-lineContents')
                    pos = fileLink.rfind("/")
                    name = fileLink[pos:]
                    fileType = name.split('.')[1] if (len(name.split('.'))>1) else name
                    path_now = "./data_type/" + fileType + "/" +path
                    filePathName = path_now + "/before" +name
                    for line in fileLines:
                        spans = line.findAll('span')
                        for span in spans:
                            text += span.get_text(strip=False)
                        text +="\n"
                    if not os.path.exists(path_now +"/before"):
                        os.makedirs(path_now +"/before")
                    with open(filePathName,"w+") as f:
                        f.write(text)
                elif first_char == "b":
                    text = ""
                    fileSoup=BeautifulSoup(urlopen(Request(fileLink,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
                    fileContents = fileSoup.find('table', class_='FileContents')
                    if not fileContents:
                        continue
                    fileLines = fileContents.findAll('td', class_='FileContents-lineContents')
                    pos = fileLink.rfind("/")
                    name = fileLink[pos:]
                    fileType = name.split('.')[1] if (len(name.split('.')) > 1) else name
                    path_now = "./data_type/" + fileType + "/" + path
                    filePathName = path_now + "/after" + name
                    for line in fileLines:
                        spans = line.findAll('span')
                        for span in spans:
                            text += span.get_text(strip=False)
                        text +="\n"
                    if not os.path.exists(path_now +"/after"):
                        os.makedirs(path_now +"/after")
                    with open(filePathName,"w+") as f:
                        f.write(text)
        return before
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return diff_to_file(diffLink,path)
        if e.code == 404:
            print("\n not found:" + diffLink+ "！")
            return ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("\n skip diff_to_file:" + diffLink+ "！")
        print(e)
        return ""

# get commit message from diff page
# return message


def diff_to_commit_message(diffLinks):
    try:
        projectSoup=BeautifulSoup(urlopen(Request(diffLinks,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        messageDiv = projectSoup.find('pre', class_='u-pre u-monospace MetadataMessage')
        message = messageDiv.get_text()
        return message
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return diff_to_commit_message(diffLink)
        if e.code == 404:
            print("\n not found:" + diffLink+ "！")
            return ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("reason", e)
        print("\n skip diff_to_project:"+diffLink+ "！")
        return ""

# get diff message from diff page
# return message


def diff_to_diff_message(diffLinks):
    try:
        projectSoup=BeautifulSoup(urlopen(Request(diffLinks,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        # more than one sometimes
        message = ""
        diffDivs = projectSoup.findAll('pre', class_='u-pre u-monospace Diff')
        for diffDiv in diffDivs:
            message = message + diffDiv.get_text() +"\n"
        return message
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return diff_to_diff_message(diffLink)
        if e.code == 404:
            print("\n not found:" + diffLink + "！")
            return ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("reason", e)
        print("\n skip diff_to_diff_message:"+diffLink+ "！")
        return ""

# get diff unified message from diff page
# return message

def diff_to_diff_unified(diffLinks):
    try:
        projectSoup=BeautifulSoup(urlopen(Request(diffLinks,
                              headers={'User-Agent': 'Mozilla/5.0'})).read(),
                              'html.parser')
        # more than one sometimes
        message = ""
        diff_unified_divs = projectSoup.findAll('pre', class_='u-pre u-monospace Diff-unified')
        for diff_unified_div in diff_unified_divs:
            diff_unified_spans = diff_unified_div.findAll('span')
            if not diff_unified_spans:
                continue
            for diff_unified_span in diff_unified_spans:
                message = message + diff_unified_span.get_text() + "\n"
        return message
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return diff_to_diff_unified(diffLink)
        if e.code == 404:
            print("\n not found:" + diffLink+ "！")
            return ""
        raise
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print("reason", e)
        print("\n skip diff_to_diff_unified:"+diffLink+ "！")
        return ""

if __name__ == "__main__":
    android_csv = pd.pandas.read_csv("uniAndroidCSV_split.csv")
    android_csv["commit_message"] = None
    android_csv["diff_message"] = None
    android_csv["diff_unified"] = None
    android_csv["project_before"] = None
    android_csv["project_after"] = None
    for index, row in android_csv.iterrows():
        commitUrl = row["codeLink"]
        diffLink = commit_to_diff(commitUrl)
        cveID = row["CVE ID"]
        main_path_str = str(index) + cveID
        if not (diffLink==""):
            # write filles
            #diff_to_file(diffLink, main_path_str)

            # a piece of commit message
            commit_message = diff_to_commit_message(diffLink)

            # diff messages (one piece)
            diff_message = diff_to_diff_message(diffLink)

            # unified diff message (one piece)
            diff_unified = diff_to_diff_unified(diffLink)

            # two links string s,s
            after, before = diff_to_project(diffLink)

            android_csv.loc[index, "commit_message"] = commit_message
            # print(commit_message)
            # print("------------------")
            android_csv.loc[index, "diff_message"] = diff_message
            # print(diff_message)
            # print("------------------")
            android_csv.loc[index, "diff_unified"] = diff_unified
            # print(diff_unified)
            # print("------------------")
            android_csv.loc[index, "project_before"] = before
            # print(before)
            # print("------------------")
            android_csv.loc[index, "project_after"] = after
            # print(after)
            # print("------------------")
            print("done", index)
    android_csv.to_csv("android_final.csv")
    print("done")