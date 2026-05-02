//DIMITRA CHRISTINA GKARAVELA AM:5051
import java.io.*;
import java.util.*;

public class RGroupBySum {

    public static void main(String[] args) throws IOException {
        String inputFile = "R.tsv";
        String outputFile = "Rgroupby.tsv";
    
        List<String> keys = new ArrayList<>();
        List<Integer> values = new ArrayList<>();
    
        BufferedReader br = new BufferedReader(new FileReader(inputFile));
        String line;
        while ((line = br.readLine()) != null) {
            String[] parts = line.split("\t");
            String key = parts[0];
            int value = Integer.parseInt(parts[1]);
            keys.add(key);
            values.add(value);
        }
        br.close();
    
        List<String> groupedKeys = new ArrayList<>();
        List<Integer> groupedValues = new ArrayList<>();
    
        mergeSortGroup(keys, values, 0, keys.size() - 1, groupedKeys, groupedValues);
    
        BufferedWriter bw = new BufferedWriter(new FileWriter(outputFile));
        for (int i = 0; i < groupedKeys.size(); i++) {
            bw.write(groupedKeys.get(i) + "\t" + groupedValues.get(i));
            bw.newLine();
        }
        bw.close();
    }
    

   
    // mergeSort 
public static void mergeSortGroup(List<String> keys, List<Integer> values,
                                  int left, int right,
                                  List<String> groupedKeys,
                                  List<Integer> groupedValues) {
    // left kai right einai san deiktes panw ston pinaka pou lene poy eisai kai 
    //pws spas tonn pinaka kathe fora
    //opote an einai isoi shmainei oti koitas se mono stoixeio 
    if (left == right) {
        groupedKeys.add(keys.get(left));
        groupedValues.add(values.get(left));
        return;
    } 

    int mid = (left + right) / 2;


    
    List<String> leftKeys = new ArrayList<>();
    List<Integer> leftValues = new ArrayList<>();
    //System.out.println("EDW KALOUME mergeSortGroupt gia left");
    mergeSortGroup(keys, values, left, mid, leftKeys, leftValues);

    List<String> rightKeys = new ArrayList<>();
    List<Integer> rightValues = new ArrayList<>();
    //System.out.println("EDW KALOUME mergeSortGroupt gia right");
    mergeSortGroup(keys, values, mid + 1, right, rightKeys, rightValues);

    //System.out.println("  MERGE left [" + left + "-" + mid + "] me right [" + (mid+1) + "-" + right + "]");
    mergeGroupedLists(leftKeys, leftValues, rightKeys, rightValues, groupedKeys, groupedValues);
    //System.out.println("  RESULT OF MERGE " + groupedKeys + " -> " + groupedValues);
}


  
    public static void mergeGroupedLists(List<String> keys1, List<Integer> values1,
                                     List<String> keys2, List<Integer> values2,
                                     List<String> mergedKeys, List<Integer> mergedValues) {
    int i = 0, j = 0;

    while (i < keys1.size() && j < keys2.size()) {
       
        String k1 = keys1.get(i);
        String k2 = keys2.get(j);
        int v1 = values1.get(i);
        int v2 = values2.get(j);

       // System.out.println("   sygkrish: " + k1 + " (" + v1 + ") vs " + k2 + " (" + v2 + ")");


        if (k1.compareTo(k2) < 0) {
            //System.out.println("Krataw : " + k1 + "\t" + v1);
            mergedKeys.add(k1);
            mergedValues.add(v1);
            i++;
        } else if (k1.compareTo(k2) > 0) {
            //System.out.println("Krataw : " + k2 + "\t" + v2);
            mergedKeys.add(k2);
            mergedValues.add(v2);
            j++;
        } else {
            int sum = v1 + v2;
            //System.out.println("Merge: " + k1 + "\t" + v1 + " + " + v2 + " -> " + sum);
            mergedKeys.add(k1);
            mergedValues.add(sum);
            i++;
            j++;
        }
    }

    //prosthiki ypoloipwn 
    while (i < keys1.size()) {
        //System.out.println("prosthetw ypoloipo apo left: " + keys1.get(i) + "\t" + values1.get(i));
        mergedKeys.add(keys1.get(i));
        mergedValues.add(values1.get(i));
        i++;
    }

    while (j < keys2.size()) {
        //System.out.println("Prosthetw ypoloipo apo right: " + keys2.get(j) + "\t" + values2.get(j));
        mergedKeys.add(keys2.get(j));
        mergedValues.add(values2.get(j));
        j++;
    }

    //System.out.println("mergedKeys" +  mergedKeys);
    //System.out.println("mergedValues" +  mergedValues);
}

}
