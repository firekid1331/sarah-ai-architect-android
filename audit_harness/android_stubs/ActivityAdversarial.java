import java.lang.reflect.*;import android.os.Bundle;import android.widget.Button;import android.widget.TextView;import org.saraharchitect.offline.MainActivity;
public class ActivityAdversarial {
 static int pass=0,fail=0;
 static void c(String s,boolean b){if(b)pass++;else {fail++;System.out.println("FAIL "+s);} }
 static Object field(Object target,String key)throws Exception{Field f=target.getClass().getDeclaredField(key);f.setAccessible(true);return f.get(target);}
 static void invoke(Object a,String name,Class<?>[] ts,Object...values)throws Exception {Method m=a.getClass().getDeclaredMethod(name,ts);m.setAccessible(true);m.invoke(a,values);}
 static String detail(Object a)throws Exception{return ((TextView)field(a,"detail")).getText();}
 public static void main(String[]args)throws Exception {
  Button.created.clear();MainActivity a=new MainActivity();invoke(a,"onCreate",new Class[]{Bundle.class},new Bundle());invoke(a,"onStart",new Class[]{});invoke(a,"onResume",new Class[]{});
  c("initial_page",(Integer)field(a,"page")==0);c("six_ui_buttons",Button.created.size()==6);
  for(int i=0;i<6;i++){Button.created.get(i).performClick();c("ui_route_"+i,(Integer)field(a,"page")==i);c("heading_"+i,((TextView)field(a,"heading")).getText().equals(org.saraharchitect.offline.ScreenModel.title(i)));}
  Button.created.get(4).performClick(); c("diagnostics_page_visible",detail(a).contains("Process-local events:"));
  String before=detail(a);invoke(a,"onPause",new Class[]{});invoke(a,"onStop",new Class[]{});invoke(a,"onStart",new Class[]{});invoke(a,"onResume",new Class[]{});
  c("lifecycle_event_retained_internal",field(a,"events").toString().contains("onResume"));
  c("live_diagnostics_repaint_after_resume_EXPECTED",!detail(a).equals(before)&&detail(a).contains("onResume"));
  Bundle save=new Bundle();invoke(a,"onSaveInstanceState",new Class[]{Bundle.class},save);Button.created.clear();MainActivity b=new MainActivity();invoke(b,"onCreate",new Class[]{Bundle.class},save);
  c("restored_diagnostics_page",(Integer)field(b,"page")==4);
  c("restored_details_match",detail(b).contains("Read-only process-local diagnostics"));
  Button.created.get(4).performClick(); c("diagnostics_page_selected",(Integer)field(b,"page")==4);
  c("new_instance_local_events",detail(b).contains("onCreate"));
  System.out.println("ACTIVITY_STUB_TESTS PASS="+pass+" FAIL="+fail);
  if(fail>0)System.exit(2);
 }
}
