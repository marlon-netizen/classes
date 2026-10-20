/* Settings for the "Faith Formation" area. Edit url and anonKey, then reload the pages.
   url / anonKey: Supabase dashboard -> Project Settings -> API (the anon/publishable key is meant to be public).
   area: keep as is - it separates this folder's students and codes from the other folders. */
window.LIA_CONFIG={
  url: 'YOUR_SUPABASE_URL',
  anonKey: 'YOUR_SUPABASE_ANON_KEY',
  area: 'faith-formation',
  areaName: 'Faith Formation',
  pages: {
    'divine-revelation-magisterium': 'Divine Revelation and the Magisterium',
    'faith-formation-exodus-covenant': 'Exodus and Covenant',
    'growing-in-values-respect': 'Respect On and Off Screen',
    'growing-in-values-road-safety': 'Road Safety in My Community',
    'growing-in-values-rules-on-wheels': 'Rules on Wheels',
    'public-ministry-of-jesus': 'Public Ministry of Jesus'
  }
};
