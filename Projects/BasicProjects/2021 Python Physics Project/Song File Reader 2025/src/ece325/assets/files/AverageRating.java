package ece325.labs.lab4;

/** 
 * Finish this class.
 */
public class AverageRating implements Comparable<AverageRating> {
	// not allowed to change anything after this (until the next marker which says you can add code again)
	private float avgRating;
	private int votes;
	
	public AverageRating(float rating, int votes) {
		this.avgRating = rating;
		this.votes = votes;
	}
		
	public float getAvgRating() {
		return avgRating;
	}
	
	public int getVotes() {
		return votes;
	}
	
	public String toString() {
		return "[AverageRating: " + avgRating + ", votes: " + votes + "]";
	}

	// You are allowed to make changes or add code after this line
	@Override
	public int compareTo(AverageRating other) {
		// Compare by rating from highest to lowest
		int ratingComparison = Float.compare(other.avgRating, this.avgRating);
		if (ratingComparison != 0) {
			return ratingComparison;
		}
		//Following return ensures we compare by votes
		return Integer.compare(other.votes, this.votes);
	}
	
	@Override
	public boolean equals(Object obj) {
		if (this == obj) return true;
		if (obj == null || getClass() != obj.getClass()) return false;
		AverageRating other = (AverageRating) obj;
		return Float.compare(other.avgRating, avgRating) == 0 && votes == other.votes;
	}
	
	@Override
	public int hashCode() {
		int ans = Float.floatToIntBits(avgRating);
		ans = 31 * ans + votes;
		return ans;
	}
}
