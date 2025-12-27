package ece325.labs.lab4;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;

/**
 * This class represents a SongCollection. You are not allowed to change the
 * code that is in between the indications, but you are allowed to add code
 * before and after the indicated lines.
 * 
 * 
 *
 */
// not allowed to change anything after this (until the next marker which says you can add code again)
public class SongCollection {
	private TreeSet<Song> collection;

	public SongCollection() {
		collection = new TreeSet<Song>();
	}

	public void addSong(Song s) {
		collection.add(s);
	}

	public String toString() {
		String str = "[SongCollection: " + collection.size() + " songs: \n";
		for (Song s : collection) {
			str += "\t" + s + "\n";
		}
		return str + "]";
	}

	/**
	 * No need to change this method. You can just call it from your main method to
	 * demonstrate that your Song class can be used in a HashSet.
	 */
	private static void demonstrateHashSetUsage() {
		Song song1 = new Song("2023", new AverageRating(8.5f, 100));
		Song song2 = new Song("2023", new AverageRating(8.5f, 100));
		Song song3 = new Song("Bridges", new AverageRating(8.9f, 150));

		Set<Song> hashSet = new HashSet<Song>();

		hashSet.add(song1);
		hashSet.add(song2);
		hashSet.add(song3);
		System.out.println("\nHashSet:");
		System.out.println(hashSet);
	}

	// You are allowed to make changes or add code after this line
	/**
	 * Load the songs in the file directly into the collection. Your implementation
	 * must use a BufferedReader and a Scanner. The songs and their ratings are in
	 * the songratings.txt file (one song per line) in the following format:
	 * Title;rating;votes 
	 * Make sure that your program doesn't break when there are
	 * malformed inputs in the input file. For this assignment, it is OK to just
	 * silently ignore any malformed inputs – your program should not cause any
	 * unhandled exceptions.
	 * 
	 * @param filename
	 */
	public void loadSongs(String filename) {
		BufferedReader reader = null;
		try {
			reader = new BufferedReader(new FileReader(filename));
			String line;
			
			while ((line = reader.readLine()) != null) {
				try {
					Scanner scanner = new Scanner(line);
					scanner.useDelimiter(";");
					
					//check if there is title
					if (!scanner.hasNext()) {
						scanner.close();
						continue;
					}
					
					String title = scanner.next().trim();
					//check if there is rating
					if (!scanner.hasNext()) {
						scanner.close();
						continue; 
					}
					
					String ratingStr = scanner.next().trim();
					
					//check missing votes
					if (!scanner.hasNext()) {
						scanner.close();
						continue;
					}
					
					String votesStr = scanner.next().trim();
					
					// Parse rating and votes
					float rating = Float.parseFloat(ratingStr);
					int votes = Integer.parseInt(votesStr);
					
					// Validate data
					if (title.isEmpty() || votes < 0 || rating < 0 || rating > 10) {
						scanner.close();
						continue;
					}
					
					// Create and add song
					AverageRating avgRating = new AverageRating(rating, votes);
					Song song = new Song(title, avgRating);
					collection.add(song);
					
					scanner.close();
				//Silently ignore x errors
				} catch (NumberFormatException e) {

					continue;
				} catch (Exception e) {
					continue;
				}
			}
		} catch (IOException e) {
			System.err.println("Error reading file: " + filename);
			System.err.println("Please ensure the file exists and is accessible.");
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException e) {
					System.err.println("Error closing file reader.");
				}
			}
		}
	}

	/**
	 * Returns a list of songs that is sorted by their average ratings.
	 * 
	 * @param comp
	 * @return
	 */
	public List<Song> sort(Comparator<Song> comp) {
		List<Song> sortedList = new ArrayList<Song>(collection);
		sortedList.sort(comp);
		return sortedList;
	}

	public static void main(String[] args) {
		// Create SongCollection and load the songs
		SongCollection coll = new SongCollection();
		coll.loadSongs("songratings.txt");

		// Print the songs in the collection and order them by average rating
		System.out.println("Songs in collection:");
		System.out.println(coll);
		System.out.println("Songs in collection ordered by average rating:");
		System.out.println(coll.sort(new SongComparator()));

		demonstrateHashSetUsage();

	}
}
