//DIMITRA CHRISTINA GKARAVELA AM:5051
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class MergeJoin {

    private int maxSizeOfBuffer = 0;

    public void mergeJoin(File fileR, File fileS, File output) throws IOException {

        //created buffer to save the matching rows
        List<String> buffer = new ArrayList<>();
        String currentJoinKey = null;

        BufferedReader readerLeft = new BufferedReader(new FileReader(fileR));   // R
        BufferedReader readerRight = new BufferedReader(new FileReader(fileS));  // S
        BufferedWriter writer = new BufferedWriter(new FileWriter(output));

        String lineLeft;
        String lineRight = readerRight.readLine(); // pointer for file S

        while ((lineLeft = readerLeft.readLine()) != null) {
            String[] fieldsLeft = lineLeft.split("\t");
            String joinKey = fieldsLeft[0];

            //an ta kleidia einai idia epanaxrhsimopoihse to buffer 
            // kai grapse thn grammh sto output file
            if (currentJoinKey != null && joinKey.equals(currentJoinKey)) {
                for (String rightRow : buffer) {
                    String[] fieldsRight = rightRow.split("\t");
                    writer.write(fieldsLeft[0] + "\t" + fieldsLeft[1] + "\t" + fieldsRight[1]);
                    writer.newLine();
                }
            } else { //pare to epomeno kleidi ws currentJoinKey kai adeiase to buffer
                currentJoinKey = joinKey;
                buffer.clear();

                // psakse tis grammes tou S gia match me to current key
                while (lineRight != null) {
                    String[] fieldsRight = lineRight.split("\t");
                    String rightKey = fieldsRight[0];
                    int cmp = joinKey.compareTo(rightKey);

                    //an to key R einai megalitero apo to kleidi ths grammhs tou S tote proxwra sto S
                    if (cmp > 0) {
                        lineRight = readerRight.readLine();
                    //an einai mikrotero tote den ehoume match (tha to eihame vrei afou einai taksinomimena)
                    } else if (cmp < 0) {
                        break;
                    } else { // einai match -> apothikeuse to buffer kai grapse sto output file
                        buffer.add(lineRight);
                        writer.write(fieldsLeft[0] + "\t" + fieldsLeft[1] + "\t" + fieldsRight[1]);
                        writer.newLine();
                        lineRight = readerRight.readLine();
                    }
                }

                // enimerwse to megisto megethos gia to buffer if needed
                if (buffer.size() > maxSizeOfBuffer) {
                    maxSizeOfBuffer = buffer.size();
                }
            }
        }

        readerLeft.close();
        readerRight.close();
        writer.close();
    }

    public static void main(String[] args) throws IOException {
        File fileR = new File(args[0]);
        File fileS = new File(args[1]);
        File output = new File(args[2]);

        MergeJoin mj = new MergeJoin();
        mj.mergeJoin(fileR, fileS, output);

        System.out.println("Max matching rows from files: " + mj.maxSizeOfBuffer);
    }
}
