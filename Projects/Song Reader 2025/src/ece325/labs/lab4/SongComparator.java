package ece325.labs.lab4;
import java.util.Comparator;

/**
 * Comparator for sorting Songs by average rating (high to low),
 * then by number of votes (high to low)
 */
public class SongComparator implements Comparator<Song> {
	
	@Override
	public int compare(Song s1, Song s2) {
		// First compare by rating high to low
		float r1 = s1.getAverageRating().getAvgRating();
		float r2 = s2.getAverageRating().getAvgRating();
		
		int ratingComparison = Float.compare(r2, r1);
		
		if (ratingComparison != 0) {
			return ratingComparison;
		}
		
		// Compare by votes
		int v1 = s1.getAverageRating().getVotes();
		int v2 = s2.getAverageRating().getVotes();
		
		return Integer.compare(v2, v1);
	}
}
