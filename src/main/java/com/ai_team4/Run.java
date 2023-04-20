package com.ai_team4;

public class Run {
    String runId;
	String gworldId;
	String teamId;
    String createT;
    String score;
    String moves;
    
    public Run(String runId, String gworldId, String teamId, String createT, String score, String moves) {
        this.runId = runId;
        this.gworldId = gworldId;
        this.teamId = teamId;
        this.createT = createT;
        this.score = score;
        this.moves = moves;
    }

    
    @Override
    public String toString() {
        return "Run [runId=" + runId + ", gworldId=" + gworldId + ", teamId=" + teamId + ", createT=" + createT
                + ", score=" + score + ", moves=" + moves + "]";
    }


    public String getRunId() {
        return runId;
    }
    public String getGworldId() {
        return gworldId;
    }
    public String getTeamId() {
        return teamId;
    }
    public String getCreateT() {
        return createT;
    }
    public String getScore() {
        return score;
    }
    public String getMoves() {
        return moves;
    }
	
	
    
}
