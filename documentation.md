# 文檔
## Login
### URL
`account/login`
#### 請求參數
|key|description|
|--------|--------|
|username|用戶名|
|password|密碼|
#### 響應參數
|key|description|
|---|-------|
|msg|阿就消息啊|

|status|description|
|----|---|
|200|成功|
|401|登陸失敗|
|500|服務器內部錯誤|

## Register
### URL
`account/register`
#### 請求參數
無
#### 響應參數
|key|description|
|---|-------|
|msg|2 forms. 1st form 'user_form' containing 3 fields(username, password1, password2). 2nd form 'student_form' containing only 1 choice field, grade.|

|status|description|
|----|---|
|200|成功|
|410|用戶名或密碼錯誤|

## Logout
### URL
`account/logout`
#### 請求參數
無
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|
---
## Enroll
### URL
`course/enroll<int:pk>`
#### 請求參數
|key|description|
|--------|--------|
|pk|primary key of the course to enroll|
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|
|404|course does not exist|

## All Courses
### URL
`course/all`
#### 請求參數
無
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|

## Available Courses (for the user)
### URL
`course/available`
#### 請求參數
無
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|

## My Courses
### URL
`course/mine`
#### 請求參數
無
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|

## Drop Course
### URL
`course/drop<int:pk>`
#### 請求參數
|key|description|
|--------|--------|
|pk|primary key of the course to drop|
#### 響應參數
|key|description|
|---|-------|
|msg|message|

|status|description|
|----|---|
|200|成功|
|404|the course does not exist|
|409|the course is not even enrolled in|
