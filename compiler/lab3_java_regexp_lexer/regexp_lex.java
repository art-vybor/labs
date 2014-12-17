import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.text.MessageFormat;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
import java.io.IOException;

public class regexp_lex  {
    public static String getPosition(String text, int offset) {
        String[] rows = text.substring(0, offset+1).split("\\n");
        return rows.length + ", " + (rows[rows.length-1].length());
    }

    public static void main(String args[]) throws IOException {
        String text = new String(Files.readAllBytes(Paths.get("source")), StandardCharsets.UTF_8);

        String bin = "[01]+b";
        String dec = "\\d+";
        String ident = "[?*|][\\d?*|]+";
        String str = "`([^`]|``)*`";
        String spaces = "[ \n\t]+";
        String error = ".";

        String[] token = {"BINARY NUMBER", "DECIMAL NUMBER", "IDENTIFIER", "STRING"};
        String pattern = String.format("(%s)|(%s)|(%s)|(%s)|(%s)|(%s)", bin, dec, ident, str, spaces, error);

        Matcher m = Pattern.compile(pattern).matcher(text);

        boolean error_lock = false;

        while (m.find()) {
            for (int i = 1; i <= m.groupCount(); ++i) {
                if (m.group(7) != null && !error_lock) {
                    System.out.printf("SYNTAX ERROR (%s)\n", getPosition(text, m.start()));
                    error_lock = true;
                    break;
                } else if (i >=1 && i <= 4) {
                    if (m.group(i) != null) {
                        System.out.printf("%s (%s): %s\n", token[i-1], getPosition(text, m.start()), m.group(i));
                        error_lock = false;
                    }

                }
            }   
        }
        
    }    
}