(import [subprocess [check_output]])
(import [time [sleep time]])
(import [os [path]])
(import [yaml [dump load]])
(import [docopt [docopt]])
(import [datetime [datetime timedelta]])
(import [tabulate [tabulate]])
(import [pyfiglet [figlet_format]])


;; Write data back to store
(defn write-data-store [store data-file]
  (with [f (open data-file "w")]
        (dump store f)))

;; Return data store; create if not exists
(defn read-data-store [data-file]
  (if (path.isfile data-file)
    (with [f (open data-file "r")]
          (load f))
    (do
     (print "data file not found, creating...")
     (let [store {}
           names (get-desktop-names (get-desktop-data))]
       (for [name names]
         (assoc store name [[]]))
       (write-data-store store data-file)
       store))))

;; Check if desktop is active
(defn desktop-active? [desktop]
  (let [state (second (.split desktop))]
    (= state "*")))

;; Get all desktop data
(defn get-desktop-data []
  (.splitlines
   (.decode (check_output ["wmctrl" "-d"]))))

;; Parse desktop names
(defn get-desktop-names [desktop-data]
  (list-comp (last (.split desktop))
             [desktop desktop-data]))

;; Get active desktop name
(defn get-active-desktop-name [desktop-data]
  (let [n (.index (list-comp
                   (desktop-active? desktop)
                   [desktop desktop-data]) True)]
    (nth (get-desktop-names desktop-data) n)))

;; Log time for given dektop
(defn log-time [store current-desktop-name data-file]
  (let [current-time (int (time))
        all-sessions (get store current-desktop-name)
        last-time (try
                   (last (last all-sessions))
                   (except [e IndexError] 0))]

    (if (= 0 last-time)
      (.pop all-sessions))
    (if (> (- current-time last-time) 120)
      (.append all-sessions [current-time])
      (.pop (last all-sessions)))

    (.append (last all-sessions) current-time)

    (assoc store current-desktop-name all-sessions)
    (write-data-store store data-file)))

;; Start logging loop
(defn start-logging-loop [data-file]
  (let [store (read-data-store data-file)]
    (while True
      (let [desktop-data (get-desktop-data)]
        (log-time store
                  (get-active-desktop-name desktop-data)
                  data-file))
      (sleep 60))))

;; Find time spent in a list of sessions starting with given timestamp
(defn time-spent [sessions from]
  (let [all []]
    (for [session sessions]
      (if (!= 0 (len session))
        (let [low (first session)
              high (last session)]
          (.append all (- high (min high (max low from)))))))
    (str (timedelta :seconds (sum all)))))

;; Return datetime at 00:00 for -nth day
(defn get-past-n-day [n]
  (let [past-date (- (datetime.today) (timedelta :days n))]
    (.replace past-date
              :hour 0
              :minute 0
              :second 0
              :microsecond 0)))

;; Return report for last n days. [oldest record, report]
(defn report [from-day data-file]
  (let [from-midnight-timestamp (.timestamp from-day)
        store (read-data-store data-file)
        desktops (get-desktop-names (get-desktop-data))
        results []
        oldest []]
    (for [desktop desktops]
      (let [sessions (get store desktop)
            first-session (first sessions)]
        (if (!= 0 first-session)
          (.append oldest (first first-session)))
        (.append results
                 [desktop
                 (time-spent sessions from-midnight-timestamp)])))
    [(min oldest) results]))

;; Main
;; -------------

(setv DATA-FILE (path.expanduser "~/dime.yaml"))
(setv DOC
      "dime | virtual desktop time tracker.
Usage:
  dime start
  dime report <last-n-days>
  dime (-h | --help)
  dime (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.")

(defn main []
  (setv arguments (docopt DOC :version "0.1.2"))

  (if (get arguments "start")
    (start-logging-loop DATA-FILE)
    (if (get arguments "report")
      (do
       (let [n (int (get arguments "<last-n-days>"))
             from-day (get-past-n-day n)
             reported-data (report from-day DATA-FILE)]
         (print (figlet_format "dime"
                               :font "rectangles"))
         (print (+ "Asked for last "
                   (str n)
                   " day(s)\nFrom : "
                   (.strftime from-day "%H:%M - %d, %b %Y\n")))
         (print (+ "[Oldest record : "
                   (.strftime (datetime.fromtimestamp
                               (first reported-data))
                              "%H:%M - %d, %b %Y]\n")))
         (print (tabulate (last reported-data)
                          :headers ["Desktop" "HH:MM:SS"]
                          :tablefmt "fancy_grid"))
         (print ""))))))
