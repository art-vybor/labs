import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.io.IOException;


public class lex  {
    public static String getPosition(String text, int offset) {
        String[] rows = text.substring(0, offset+1).split("\\n");
        return rows.length + ", " + (rows[rows.length-1].length());
    }

    public static void main(String args[]) throws IOException {
        String text = new String(Files.readAllBytes(Paths.get("source")), StandardCharsets.UTF_8);

        Lexer lex = new Lexer(text);

        System.out.println("Tokens:");        
        Token token = lex.nextToken();        
        while (token != null) {
            System.out.printf("\t%s\n", token);
            token = lex.nextToken();
        }

        System.out.println("Comments:");
        for (String comment : lex.getComments()) {
            System.out.printf("\t%s\n", comment);
        }
        
        System.out.println("Errors:");
        for (String error : lex.getErrors()) {
            System.out.printf("\t%s\n", error);
        }
    }    
}