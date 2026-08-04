# Catalogue Search and Private-Shelf Import Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Reader
    participant View as BookSearchView / BookImportView
    participant Service as Open Library Service
    participant Signer as Django Signing
    participant Catalog as CatalogBook
    participant Shelf as Book

    Reader->>View: Search title, author or ISBN
    View->>Service: search(query)
    Service-->>View: normalised results
    View->>Signer: sign selected result payload
    View-->>Reader: results with import token
    Reader->>View: POST signed token
    View->>Signer: verify token
    alt token invalid or expired
        View-->>Reader: reject request
    else token valid
        View->>Catalog: get or create canonical book
        View->>Shelf: get or create owner + catalogue entry
        View-->>Reader: open private shelf entry
    end
```

The external response is never trusted as an ownership decision. Import metadata is signed before round-tripping through the browser, canonical catalogue data is reused, and the authenticated server-side user becomes the shelf owner.
