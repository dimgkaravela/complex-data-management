//DIMITRA CHRISTINA GKARAVELA AM:5051
import java.io.*;

public class Union {

    public void union(File fileR, File fileS, File output) throws IOException {
        BufferedReader readerR = new BufferedReader(new FileReader(fileR));
        BufferedReader readerS = new BufferedReader(new FileReader(fileS));
        BufferedWriter writer = new BufferedWriter(new FileWriter(output));

        String rLine = readerR.readLine();
        String sLine = readerS.readLine();

        String lastWritten = null;

        while (rLine != null || sLine != null) {
            String candidate;

            //an rLine <= sLine -> pare to rLine gia candidate kai proxwra sto R arxeio
            if (rLine != null && (sLine == null || rLine.compareTo(sLine) <= 0)) {
                candidate = rLine;
                rLine = readerR.readLine();
            } else { // an einai megalitero pare to sLine gia candidate kai proxwra sto S arxeio
                candidate = sLine;
                sLine = readerS.readLine();
            }

            // elegxos gia duplicate 
            if (lastWritten == null || !candidate.equals(lastWritten)) {
                writer.write(candidate);
                writer.newLine();
                lastWritten = candidate;
            }
        }

        readerR.close();
        readerS.close();
        writer.close();
    }

    public static void main(String[] args) throws IOException {
        File fileR = new File(args[0]);
        File fileS = new File(args[1]);
        File output = new File(args[2]);

        Union unionInstance = new Union();
        unionInstance.union(fileR, fileS, output);
    }
}
