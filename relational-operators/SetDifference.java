//DIMITRA CHRISTINA GKARAVELA AM:5051
import java.io.*;

public class SetDifference {

    public void difference(File fileR, File fileS, File output) throws IOException {
        BufferedReader readerR = new BufferedReader(new FileReader(fileR));
        BufferedReader readerS = new BufferedReader(new FileReader(fileS));
        BufferedWriter writer = new BufferedWriter(new FileWriter(output));

        String rLine = readerR.readLine();
        String sLine = readerS.readLine();
        String lastWritten = null;

        while (rLine != null && sLine != null) {
            int cmp = rLine.compareTo(sLine);
            if (cmp < 0) {
                // rLine mono sto R
                if (lastWritten == null || !rLine.equals(lastWritten)) {
                    writer.write(rLine);
                    writer.newLine();
                    lastWritten = rLine;
                }
                rLine = skipDuplicates(readerR, rLine);
            } else if (cmp == 0) {
                // koih grammh kai sta dyo -> skip both
                rLine = skipDuplicates(readerR, rLine);
                sLine = skipDuplicates(readerS, sLine);
            } else {
                // sLine < rLine proxwra parakatw sto S
                sLine = skipDuplicates(readerS, sLine);
            }
        }

        // oi ypoloipes grammes tou R einai pithano apotelesma
        while (rLine != null) {
            if (lastWritten == null || !rLine.equals(lastWritten)) {
                writer.write(rLine);
                writer.newLine();
                lastWritten = rLine;
            }
            rLine = skipDuplicates(readerR, rLine);
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

        SetDifference md = new SetDifference();
        md.difference(fileR, fileS, output);
    }
}
