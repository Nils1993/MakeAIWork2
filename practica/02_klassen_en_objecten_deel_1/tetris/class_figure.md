```mermaid
classDiagram
    class Figure {
        -color: str    
        -shape: Numpy Array
        +init(shape, color)
        +getColor(): str
        +getShape(): Numpy Array 
        +rotate()
    }
```