//DIMITRA CHRISTINA GKARAVELA AM:5051
import java.io.*;

public class Intersection {

    public void intersection(File fileR, File fileS, File output) throws IOException {
        BufferedReader readerR = new BufferedReader(new FileReader(fileR));
        BufferedReader readerS = new BufferedReader(new FileReader(fileS));
        BufferedWriter writer = new BufferedWriter(new FileWriter(output));

        String rLine = readerR.readLine();
        String sLine = readerS.readLine();
        String lastWritten = null;

        while (rLine != null && sLine != null) {
            int cmp = rLine.compareTo(sLine);
            //mikroterh
            if (cmp < 0) {
                rLine = skipDuplicates(readerR, rLine);
            } else if (cmp > 0) { //megaliterh
                sLine = skipDuplicates(readerS, sLine);
            } else { // idies ara ehoume koino stoixeio -> grafetai sto output
                if (lastWritten == null || !rLine.equals(lastWritten)) {
                    writer.write(rLine);
                    writer.newLine();
                    lastWritten = rLine;
                }
                rLine = skipDuplicates(readerR, rLine);
                sLine = skipDuplicates(readerS, sLine);
            }
        }

        readerR.close();
        readerS.close();
        writer.close();
    }

    private String skipDuplicates(BufferedReader reader, String current) throws IOException {
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.equals(current)) {
                return line;
            }
        }
        return null;
    }

    public static void main(String[] args) throws IOException {
        File fileR = new File(args[0]);
        File fileS = new File(args[1]);
        File output = new File(args[2]);

        Intersection mi = new Intersection();
        mi.intersection(fileR, fileS, output);
    }
}
