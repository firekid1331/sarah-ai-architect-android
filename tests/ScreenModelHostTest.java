import org.saraharchitect.offline.ScreenModel;
public class ScreenModelHostTest {public static void main(String[] args){
 for(int i=0;i<ScreenModel.pageCount();i++){if(ScreenModel.validPage(i)!=i)throw new AssertionError("route "+i);if(ScreenModel.content(i).isEmpty())throw new AssertionError("empty "+i);}
 String[] labels=ScreenModel.labels(); labels[0]="CORRUPTED"; if(ScreenModel.label(0).equals("CORRUPTED"))throw new AssertionError("mutable labels");
 String[] titles=ScreenModel.titles(); titles[0]="CORRUPTED"; if(ScreenModel.title(0).equals("CORRUPTED"))throw new AssertionError("mutable titles");
 if(ScreenModel.validPage(-1)!=0||ScreenModel.validPage(99)!=0)throw new AssertionError("bounds");
 if(!ScreenModel.content(3).contains("DISABLED"))throw new AssertionError("link");
 System.out.println("PASS 6 routes + 2 bounds + disabled link");}}
