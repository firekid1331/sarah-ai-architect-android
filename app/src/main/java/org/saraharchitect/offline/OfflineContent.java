package org.saraharchitect.offline;

/** Pure local static content: no network, no native hooks and no authority. */
public final class OfflineContent {
  private OfflineContent() {}
  public static final String RELEASE = "M2 v0.1.1 HOST CANDIDATE / NOT INSTALL AUTHORIZED";
  public static final String SAFETY = "NO NETWORK • NO MINECRAFT LINK • NO AI TOOLS • NO WORLD EDITS";
  public static final String OVERVIEW = "SARAH AI Architect\n\nDedicated Android application prototype.\n\n"+
      "This screen is static and offline. It does not talk to Sarah's Minecraft NPC.\n\n"+
      "Building an APK through GitHub is NOT permission to install or use it.\n";
  public static final String ARCHITECTURE = "Architecture Studio — planned\n\n"+
      "Future: conceptual sketches, city districts, underground layouts and structured plan previews.\n\n"+
      "No planning engine is embedded in this APK candidate. No Minecraft blocks are generated.";
  public static final String EVIDENCE = "Audit status — frozen evidence\n\n"+
      "P01.4A R04: TARGETED_HOST_CORRECTIONS_VERIFIED (mock only).\n"+
      "P014A-LIMIT-003: OPEN (rollback-resistant durable nonce storage).\n"+
      "P011-PROVENANCE: OPEN (real owner and world identity).\n"+
      "Local Link L01.2: host-only targeted fixes verified; no device connection.\n\n"+
      "No operational approval is granted by this display.";
  public static final String DIAGNOSTICS = "Read-only process-local diagnostics.\nNo external identity, world access or device attestation.";
  public static final String ABOUT = "SARAH v0.1.1 host candidate\nPackage: org.saraharchitect.offline\nBuild source: preserved M2 Build #3 archive (local development derivative)\nAPK SHA-256: NOT ATTESTED IN APP\nSigning identity: NOT ATTESTED IN APP\n\nAndroid Home = circle; Recents = square; Back = triangle. These are Android system controls, not app buttons.\n\nNot authorized to install or test on device.";
  public static final String CONNECTION = "Minecraft Link — DISABLED\n\n"+
      "Android /wsserver on same phone remains unproven.\n"+
      "This build includes no listener, no WebSocket code, no Internet permission and no foreground service.\n\n"+
      "Do not attempt a Minecraft connection under this milestone.";
}
