# python-twiki

python-twiki is a bunch of tools which allow manage a TWiki.

# Examples

## Configuration file (setup.cfg)

```
auth:http_basic
auth_user:psaavedra
auth_password:verysecret
url:https://localhost/
```
where `url` is something like: ''https://wiki.igalia.com/twiki''.

In other side, `auth` and `auth_*` settings refer to HTTP Basic
authentication parameters, in necessary case.

## Getting Topics from a Web

```sh 
$ twiki-get-topics -c setup.cfg -o list.csv -w WebName

```

where `list.csv` results something like this:

```
"WebName/WebTopic1",
"WebName/WebTopic2",
```

## Moving a Topic to another Topic parent

```sh
$ twiki-move-topic -c setup.cfg -t WebName/WebTopic -p NewWebTopicParent
$ twiki-move-topic -c setup.cfg -i list.csv
$ twiki-move-topic -c setup.cfg -i list.csv -p NewWebTopicParent

```

where `list.csv` is something like this:

```
"WebName/WebTopic1", "NewWebTopicParent1"
"WebName/WebTopic2", "NewWebTopicParent2"

```

## Renaming Topics

```sh
$ twiki-rename-topic -c setup.cfg -t WebName/WebTopic -n NewWebName/NewWebTopic
$ twiki-rename-topic -c setup.cfg -i list.csv
```

where `list.csv` is something like this:

```
"WebName/WebTopic1", "NewWebName/NewWebTopic1"
"WebName/WebTopic2", "NewWebName/NewWebTopic2"
```


