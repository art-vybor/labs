import java.lang.Character;


public class Position implements Cloneable {
    private String text;
    private int line;
    private int position;
    private int index;
    private final char EOF_char = 0x01;

    public Position(String text) {
        this.text = text + EOF_char;
        line = 1;
        position = 1;
        index = 0;
    }

    public boolean isNewLine() {
        if (text.charAt(index) == EOF_char)
            return true;

        return text.charAt(index) == '\n';
    }

    public boolean isWhiteSpace() {
        return Character.isWhitespace(text.charAt(index));
    }

    public boolean isLatinLetter() {
        char c = text.charAt(index);
        return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
    }

    public boolean EOF() {
//System.out.printf("EOF(%c): %s, %d\n", EOF_char, text, index);
        return text.charAt(index) == EOF_char;
    }

    public Position next() {
        if (index < text.length()) {
            if (isNewLine()) {
                line++;
                position = 1;
            } else {
                if (Character.isHighSurrogate(text.charAt(index)))
                    index++;
                position++;
            }
            index++;
        }
        return this;
    }

    public String getTextTo(Position end) {
        return text.substring(index, end.getIndex()+1);
    }

    public char getCharacter() {
        return text.charAt(index);
    }

    public int getLine() {
       return line;
    }

    public int getPosition() {
       return position;
    }

    public int getIndex() {
       return index;
    }

    @Override
    public String toString() {
        return String.format("(%d, %d)", line, position);
    }

    @Override
    public Position clone() {
        try {
            return (Position) super.clone();
        }
        catch (CloneNotSupportedException e) {
            return null;
        }
    }

}
