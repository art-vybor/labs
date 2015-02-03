enum DomainTag {
    Comment,
    Ident,
    Keyword,
    Space
}

public class Token
{    
    private Position begin;
    private Position end;

    private DomainTag tag;
    
    public Token(DomainTag tag, Position begin, Position end)
    {
        this.tag = tag;
        this.begin = begin.clone();
        this.end = end.clone();
    }

    @Override
    public String toString() {
        String value = begin.getTextTo(end);
        return String.format("%s %s-%s: %s", tag, begin, end, value);
    }
}