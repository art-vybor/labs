import java.util.*;

public class Lexer {
    private String text;
    private Position position;
    private List<String> Errors = new ArrayList<String>();
    private List<String> Comments = new ArrayList<String>();


    public Lexer(String text)
    {
        this.text = "";

        Position tmp_position = new Position(text);
        StringBuffer textBuffer = new StringBuffer();

        while (!tmp_position.EOF()) {
            char c = tmp_position.getCharacter();
            if (tmp_position.isLatinLetter() || tmp_position.isNewLine() || tmp_position.isWhiteSpace() || c == '*')
                textBuffer.append(c);
            else {
                Errors.add(String.format("Error %s: incorrect symbol (%c)", tmp_position, c));
                textBuffer.append(' ');
            }
            tmp_position.next();
        }
        
        this.text = textBuffer.toString();
        position = new Position(this.text);
    }

    public Token nextToken() {
//System.out.printf("nextToken pos:%s\n", position);
        while (!position.EOF()) {
            
            while (position.isWhiteSpace()) position.next();

            Position start = position.clone();
//System.out.println("start: " + start);
            Position end = position.clone();

            switch (position.getCharacter()) {
                case '*':
                    if (position.getPosition() == 1) {                        
                        while (!position.next().isNewLine())
                            end = position.clone();
                        Comments.add(String.format("%s-%s", start, end));
                        break;
                    }
                    
                    end = position.next().clone();
                    if (position.getCharacter() == '*') {
                        if (position.clone().next().getCharacter() != '*') {
                            position.next();
                            return new Token(DomainTag.Keyword, start, end);
                        } else {
                            while (position.next().getCharacter() == '*') end = position.clone();
                            return new Token(DomainTag.Ident, start, end);
                        }
                    } else {
                        return new Token(DomainTag.Ident, start, start);
                    }                    
                case 'w':
                case 'e':
                    Position tmp_position = position.clone();
                    
                    if (position.getCharacter() == 'w') {
                        if (tmp_position.next().getCharacter() == 'i' && tmp_position.next().getCharacter() == 't' && tmp_position.next().getCharacter() == 'h') {
                            position.next().next().next().next();
                            return new Token(DomainTag.Keyword, start, tmp_position);
                        }
                    } else {
                        if (tmp_position.next().getCharacter() == 'n' && tmp_position.next().getCharacter() == 'd') {
                            position.next().next().next();
                            return new Token(DomainTag.Keyword, start, tmp_position);
                        }
                    }
                default:
                    end = position.clone();
                    while (position.next().isLatinLetter()) end = position.clone();

                    if ((position.getIndex() - start.getIndex()) % 2 == 1)
                        return new Token(DomainTag.Ident, start, end);
                    else 
                        Errors.add(String.format("Error %s: %s", start, "incorrect ident (an even number of Latin characters)"));
                        break;
            }
        }
        return null;
    }

    public List<String> getErrors() {
        return Errors;
    }

    public List<String> getComments() {
        return Comments;
    }


}
