# Exercise Tracker

Your responses should have the following structures.

Exercise:

```
{
  username: "fcc_test"
  description: "test",
  duration: 60,
  date: "Mon Jan 01 1990",
  _id: "5fb5853f734231456ccb3b05"
}
```
User:

```
{
  username: "fcc_test",
  _id: "5fb5853f734231456ccb3b05"
}
```
Log:

```
{
  username: "fcc_test",
  count: 1,
  _id: "5fb5853f734231456ccb3b05",
  log: [{
    description: "test",
    duration: 60,
    date: "Mon Jan 01 1990",
  }]
}
```

Hint: For the date property, the toDateString method of the Date API can be used to achieve the expected output.