package org.saraharchitect.offline;
import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
/** Offline-only informational UI. No permissions, network, or world APIs. */
public final class MainActivity extends Activity {
 private static final String STATE_PAGE="sarah.selectedPage";
 private int page=0;
 private String lastTransition="created";
 private final StringBuilder events=new StringBuilder();
 private TextView heading,detail,diagnostics;
 private int dp(int x){return Math.round(x*getResources().getDisplayMetrics().density);}
 private TextView label(String s,int size,int color){TextView v=new TextView(this);v.setText(s);v.setTextSize(size);v.setTextColor(color);return v;}
 private void event(String s){lastTransition=s;if(events.length()>360)events.delete(0,events.length()-240);events.append(s).append("\n");}
 private void select(int p){page=ScreenModel.validPage(p);event("page:"+page);render();}
 private void refreshDiagnostics(){if(page==4 && detail!=null)render();}
 private void render(){if(heading==null)return;heading.setText(ScreenModel.title(page));
   detail.setText(ScreenModel.content(page));
   if(page==4)detail.setText(OfflineContent.DIAGNOSTICS+"\n\nCurrent page: "+page+"\nLast transition: "+lastTransition+"\nProcess-local events:\n"+events);
 }
 @Override public void onCreate(Bundle state){super.onCreate(state);event("onCreate");
   if(state!=null)page=ScreenModel.validPage(state.getInt(STATE_PAGE,0));
   ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);
   LinearLayout root=new LinearLayout(this);root.setOrientation(1);root.setPadding(dp(20),dp(24),dp(20),dp(24));root.setBackgroundColor(Color.rgb(16,24,34));scroll.addView(root);setContentView(scroll);
   TextView logo=label("SARAH",32,Color.WHITE);logo.setTypeface(Typeface.DEFAULT,Typeface.BOLD);root.addView(logo);
   TextView subtitle=label("AI ARCHITECT / M2 v0.1.1 HOST CANDIDATE",12,Color.rgb(132,199,190));root.addView(subtitle);
   TextView safety=label("OFFLINE PROTOTYPE • MINECRAFT LINK DISABLED • AI TOOLS DISABLED • CONSTRUCTION DISABLED",13,Color.rgb(250,213,128));safety.setPadding(0,dp(15),0,dp(15));root.addView(safety);
   for(int i=0;i<ScreenModel.pageCount();i++){final int p=i;Button b=new Button(this);b.setText(ScreenModel.label(i));b.setAllCaps(false);b.setOnClickListener(v->select(p));root.addView(b);}
   heading=label("",22,Color.WHITE);heading.setPadding(0,dp(16),0,dp(6));root.addView(heading);
   detail=label("",15,Color.rgb(216,229,234));root.addView(detail);
   TextView footer=label(OfflineContent.RELEASE,11,Color.rgb(139,160,171));footer.setGravity(Gravity.CENTER);footer.setPadding(0,dp(25),0,0);root.addView(footer);render();
 }
 @Override protected void onStart(){super.onStart();event("onStart");refreshDiagnostics();}
 @Override protected void onResume(){super.onResume();event("onResume");refreshDiagnostics();}
 @Override protected void onPause(){event("onPause");refreshDiagnostics();super.onPause();}
 @Override protected void onStop(){event("onStop");refreshDiagnostics();super.onStop();}
 @Override protected void onSaveInstanceState(Bundle out){out.putInt(STATE_PAGE,page);event("onSaveInstanceState");refreshDiagnostics();super.onSaveInstanceState(out);}
 @Override protected void onDestroy(){event("onDestroy");super.onDestroy();}
}
