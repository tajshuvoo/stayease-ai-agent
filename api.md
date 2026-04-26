# API Contract

---

## 1. POST /api/chat/{conversation_id}/message

Send a guest message to the AI agent.

### Request Schema

```
{
  "message": "string"
}
```

### Response Schema
```
{
  "response": "string",
  "data": "object | null"
}
```
### Example

#### Request

```POST /api/chat/conv_001/message```
```
{
  "message": "I need a room in Cox's Bazar for 2 nights for 2 guests"
}
```

#### Response
```
{
  "response": "Here are available properties in Cox's Bazar:",
  "data": [
    {
      "listing_id": 101,
      "title": "Sea View Apartment",
      "price_per_night": 4500,
      "currency": "BDT"
    },
    {
      "listing_id": 102,
      "title": "Beachside Resort Room",
      "price_per_night": 6000,
      "currency": "BDT"
    }
  ]
}
```

### Possible Errors
```
{
  "error": "Invalid input message"
}
```
-400 Bad Request → Missing or invalid message
-404 Not Found → Conversation ID does not exist
-500 Internal Server Error → Unexpected failure

## 2. GET /api/chat/{conversation_id}/history

Retrieve full conversation history.

### Request

```GET /api/chat/conv_001/history```

### Response Schema
```
{
  "conversation_id": "string",
  "messages": [
    {
      "role": "user | assistant",
      "content": "string"
    }
  ]
}
``` 

#### Example Response
```
{
  "conversation_id": "conv_001",
  "messages": [
    {
      "role": "user",
      "content": "I need a room in Cox's Bazar"
    },
    {
      "role": "assistant",
      "content": "Here are available properties in Cox's Bazar..."
    },
    {
      "role": "user",
      "content": "Tell me details about listing 101"
    },
    {
      "role": "assistant",
      "content": "Sea View Apartment costs 4500 BDT per night..."
    }
  ]
}
```

### Possible Errors
```
{
  "error": "Conversation not found"
}
```
- 404 Not Found → Conversation ID does not exist
- 500 Internal Server Error → Unexpected failure