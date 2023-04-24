
# AlterMovie

My technical test for Alternova




## Tech Stack

**Frontend & Backend:**  Python, Django


## Screenshots
**Home Page**
![App Screenshot](https://i.imgur.com/9gNgzJl.jpg)

**All audiovisual productions**
![App Screenshot](https://i.imgur.com/I1CbOBD.jpg)

**Only Movies**
![App Screenshot](https://i.imgur.com/uEmsfNE.jpg)

**Only Series**
![App Screenshot](https://i.imgur.com/vxyKRd4.jpg)

**Random audiovisual production**
![App Screenshot](https://i.imgur.com/sY1Ex4O.jpg)
## API Reference

#### Get all items

```http
  GET /api/v1/items/
```
Returns all media items
| Parameter | Description                |
| :-------- | :------------------------- |
| ?type   | get all items by time |
| ?name    | get all items by name |
| ?genre    | get all items by genre |


#### Get item random

```http
  GET /api/v1/items/random/
```
Return a random item
| Parameter | Description                       |
| :-------- | :-------------------------------- |
|   |  |

#### Get items ordered

```http
  GET api/v1/items/:type_prod/:order/
```
Returns all items sorted by parameter and search type
| Parameter | Description                       |
| :-------- | :-------------------------------- |
| :type_prod    | Type of media Movie/Serie |
| :order    | param for order name/genre/views/rating |

#### Get user interactions

```http
  GET api/v1/userinteractions/:id/
```
Returns all interactions made by the user with media
| Parameter | Description                       |
| :-------- | :-------------------------------- |
| :id   | User ID |

#### Mark media like viewed

```http
  GET api/v1/userinteractions/viewed/<int:id>/
```

| Parameter | Description                       |
| :-------- | :-------------------------------- |
| :id   | ID Movie/Serie |

#### Rating a media

```http
  GET api/v1/userinteractions/rate/<int:id>/
```

| Parameter | Description                       |
| :-------- | :-------------------------------- |
| :id   | ID Movie/Serie |

## Coded by Brycot with 💙



