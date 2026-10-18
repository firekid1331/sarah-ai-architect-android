package org.saraharchitect.offline;
/** Pure, deterministic offline page router, no Android dependency. */
public final class ScreenModel {
 private static final String[] LABELS={"Overview","Architecture","Audit evidence","Minecraft link","Diagnostics","About / Test instructions"};
 private static final String[] TITLES={"Dashboard","Design studio","Verification status","Connection status","Diagnostics","About / Test instructions"};
 public static final int DEFAULT_PAGE=0;
 private ScreenModel() {}
 public static int pageCount(){return LABELS.length;}
 public static String label(int page){return LABELS[validPage(page)];}
 public static String title(int page){return TITLES[validPage(page)];}
 public static String[] labels(){return LABELS.clone();}
 public static String[] titles(){return TITLES.clone();}
 public static int validPage(int page){return page>=0 && page<LABELS.length?page:DEFAULT_PAGE;}
 public static String content(int page){switch(validPage(page)){
 case 1:return OfflineContent.ARCHITECTURE;
 case 2:return OfflineContent.EVIDENCE;
 case 3:return OfflineContent.CONNECTION;
 case 4:return OfflineContent.DIAGNOSTICS;
 case 5:return OfflineContent.ABOUT;
 default:return OfflineContent.OVERVIEW;}}
}
