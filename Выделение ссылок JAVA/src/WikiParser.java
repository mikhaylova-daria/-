import edu.jhu.nlp.wikipedia.PageCallbackHandler;
import edu.jhu.nlp.wikipedia.WikiPage;
import edu.jhu.nlp.wikipedia.WikiXMLParser;
import edu.jhu.nlp.wikipedia.WikiXMLParserFactory;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.Writer;

/**
 * Вычленение ссылок для каждой статьи википедии в отдельный файл
 */

public class WikiParser {
    static int i = 0;
    public static void main(String[] args) throws Exception {
        WikiXMLParser wxsp = WikiXMLParserFactory.getSAXParser("/home/daria/enwiki-20150304-pages-articles.xml.bz2");
        try {
            wxsp.setPageCallback(new PageCallbackHandler() {
                public void process(WikiPage page) {
                    ++i;
                    try {
                    Writer writer = new BufferedWriter(new OutputStreamWriter(
                            new FileOutputStream("/home/daria/Links/" + page.getTitle()), "utf-8"));
                    for (String link :  page.getLinks()) {
                        writer.write(link + "\n");
                    }
                    writer.close();
                    } catch (Exception e) {

                    }
                    if (i == 5000) {
                        System.exit(0);
                    }
                }
            });
            wxsp.parse();

        } catch(Exception e) {
            e.printStackTrace();
        }

    
    }
}
