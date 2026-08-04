# Reading Compass Domain Class Diagram

```mermaid
classDiagram
    User "1" --> "0..*" Book : owns shelf entries
    User "1" --> "0..*" PublicReview : writes
    User "1" --> "0..*" ReadingList : curates
    User "1" --> "0..*" ForumPost : writes
    User "1" --> "0..*" ForumReply : writes
    CatalogBook "1" --> "0..*" Book : referenced by
    CatalogBook "0..*" --> "0..*" Category : tagged with
    CatalogBook "1" --> "0..*" PublicReview : receives
    CatalogBook "1" --> "0..1" Forum : has
    CatalogBook "0..*" --> "0..*" ReadingList : included in
    Book "1" --> "0..*" ReadingNote : contains private notes
    Forum "1" --> "0..*" ForumPost : contains
    ForumPost "1" --> "0..*" ForumReply : contains

    class CatalogBook {
      title
      author
      isbn_10
      isbn_13
      cover_url
    }
    class Book {
      owner
      catalog_book
      status
    }
    class ReadingList {
      owner
      name
      is_public
    }
    class PublicReview {
      author
      rating
      content
    }
    class RecommendationDismissal
    class Forum
    class ForumPost
    class ForumReply
```

## Design interpretation

The shared `CatalogBook` prevents repeated metadata. `Book` is the private owner-to-catalogue relationship and holds reading status; `ReadingNote` remains below that private boundary. Reviews, public lists and forums attach to catalogue books so community content is shared deliberately. Unique constraints prevent duplicate shelf entries, duplicate reader reviews, duplicate dismissals and multiple forums for one book.
