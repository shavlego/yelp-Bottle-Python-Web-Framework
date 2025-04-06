
ΣΧΕΔΙΑΣΗ ΚΑΙ ΧΡΗΣΗ ΒΑΣΕΩΝ ΔΕΔΟΜΕΝΩΝ 2019-2020

ΕΡΓΑΣΙΑ 2
Bottle: Python Web Framework


1) Shavlego Mnatobishvili
A.M:1115201200113




ΠΑΡΑΤΗΡΗΣΕΙΣ

ΜΕΡΟΣ ΠΡΩΤΟ

Στο 1ο μέρος έχουμε προσαρμόσει τα ερωτήματα ώστε να δίνουν τα αποτελέσματα
με τη μορφή των ενδεικτικών λύσεων που μας δόθηκαν.

Το ερώτημα 4 για να επιστραφεί μόνο το πλήθος των επιχειρήσεων, θα μπορούσε
να γραφεί και ως εξής:

select count(business_id) from (
    select r.business_id
    from reviews r, reviews_pos_neg r_pn
    where r.review_id = r_pn.review_id and r.date >= '2014-01-01'
    and r.date <= '2014-12-31'
    group by r.business_id
    having count(r_pn.positive) > 10 ) as tmp;

Το ερώτημα 6 για να εμφανίζεται μόνο μια φορά το id της επιχείρησης θα μπορούσε
να γραφεί και ως εξής:

select sum(r.votes_useful) as sum_votes_useful, r.user_id, b.name
from reviews r, business b
where r.business_id = b.business_id and b.name = 'Midas'
group by r.business_id
order by sum_votes_useful desc;

ΜΕΡΟΣ 2ο

Τα δεδομένα που δίνονται μέσω του web interface δεν πρέπει να περιέχουν quotes
(') διαφορετικά προκύπτει sql exception (τυπώνεται ανάλογο debug μήνυμα) στην
κονσόλα.

1. classify_review:

Ενδεικτικά αποτελέσματα:

4yFQbjq9DtIoY3bxpznMLg -> negative
7bH_639rr5qSSv1-BI4zAw -> positive
GVgzJAtCL96WgC2lxuTGdw -> neutral (0 στον πίνακα reviews_pos_neg)
OiWFpcrUJZrSdHztTpdD0w -> positive
Qf5ZqTblnQ0kSc2GEdmzbA -> negative

Έγινε έλεγχος του αλγορίθμου μας σε σχέση με ολόκληρο τον πίνακα reviews_pos_neg
με την συνάρτηση test_classify_review() και τα αποτελέσματα συμφωνούν κατά 
97% περίπου.

2. update_zip_code:

Επιστρέφει "οκ" εφόσον υπάρχει το business_id ακόμα κι αν είναι το νέο zip code 
είναι ίδιο με το παλιό. Αν δεν βρεθεί το business_id ή προκύψει κάποιο άλλο
σφάλμα επιστρέφει "error".

3. selectTopNbusinesses:

Το Ν πρέπει να είναι ακέραιος διαφορετικά προκύπτει exception (TypeError).

Αν οι επιχειρήσεις στην επιλεγείσα κατηγορία είναι λιγότερες από Ν, τότε
επιστρέφει όλες τις επιχειρήσεις

Ενδεικτικά αποτελέσματα:

Category Id: 1, N: 10

results = 
business_id	numberOfreviews
qMkIbQFrROSnPaQ7at85-w	101
X3icXUyW9vS4UXY6V_MR4w	47
1Ap6ZNCvyLLKHP0wvCk9yA	44
kEsKrIJ6M1KOb8UALrpP7g	44
PoRYjYUSjmeWM1WLsx_45w	39
Uxd43FDZnBoeRFPz0b7Ohw	31
CPVipBqeuxWt8UzskKnDWg	25
wGAehOy0jG02k_FS5sx8CQ	25
0NaMndmNpVG619STpRCY7Q	24
3KJYJGJf5qoUfuK7dCWzPA	22


4. traceUserInfluence:

Το Depth πρέπει να είναι ακέραιος διαφορετικά προκύπτει exception (TypeError).

Αν ο χρήστης δεν επηρεάζει κάποιον άλλο χρήστη στο δοθέν βάθος, τότε η 
συνάρτηση εκτυπώνει ανάλογο μήνυμα στην κονσόλα και επιστρέφει μόνο τα header.

Ενδεικτικά αποτελέσματα:

User id: --65q1FpAL_UQtVZ2PTGew
Depth: 3

results =
user_id
7GC9fVWKa4a1ZmBGLH6Uww
fPHLPrymsyb6WSFFKoMrTQ
q9XgOylNsSbqZqF_SO3-OQ
8JC-Yb3UDUv2FUl5ym1nVg
wNqwKWaRjClmcKsoJJRFow
ast7yCfvhIwaD53OFSXoag
IO3AsR6cdMto7VCwfPzf2w
i0A-c2yoHySmFhRV2sDR1g
Gsl8Rv_1aUQEHOm-2zh8MQ
XeoAojoz5johV2MQ5ngNig
d66FhQQZzFDKxklh6t63RA
XqMkm-DD9VsdcKx2YVGhSA
jdeNI5TTTuM6mj3HTgstRA
azj8vFl7JuSyHqamSVhd4A
palND-kF1qpMLhkcgAnSxA
-kIvLyWpY17aRa0vPp-RmA
wVSGZN8d3ao4ad97kEDzYg
IDHrwv_RCildFvmfWTkj5Q
X5GbNXY_nNoa_vTZDD0aCA
sDyaN_3DEZyhnJPUFIwoEg
VexAJmqOClKzm8KbY7xs5g
APLIPfq1Rf8QyhHHk2uAyA
E5QyEU6FCQwnTys0S73zNw
l81ILmOhky5bG7o4r3rkhQ
N1Q6HiZvnZHjNU712Gymqw
Lp_Ykqfbv5Q-oyGYlMGJRg
--65q1FpAL_UQtVZ2PTGew
nitmbm5VgwHCDSr2hZkUZw
e-GOQDdx_pPSi_dHJ87oKQ
2AbBZM7n9EMwa0nK1yl0CA
ST8Yzlk2MqKlcaLqL2djBg
palND-kF1qpMLhkcgAnSxA
eY9ZXESFPjhZf4rUFkssFQ
jdeNI5TTTuM6mj3HTgstRA
IDHrwv_RCildFvmfWTkj5Q
QbviJe9Vu89yaQEV4KCb_w
y8ZCNq8HSGDSx7Vm-NYEOw
xdl61MWMguYRSunH8CniQw
NfLyune1sAOVrHUAeQ9L-g
wy8Yd_vCWDjiz9rMo4HfqA
_w9Heqb4e-597dC-3JP_qg
X5GbNXY_nNoa_vTZDD0aCA
hORy0O17fXiPM5g_ouY3-A
wpqpfX_ueU6MH2_jlQgnkg
yEQ96ibrgRxUaJP_wv5cbw
WGTEuxi9I5LBLjdUB7Pk_Q
sDyaN_3DEZyhnJPUFIwoEg
VexAJmqOClKzm8KbY7xs5g
ZGfbxU-9wtRDTrfLRzfiMQ
HestW1GKSkmUs_vpnauE_w
2AbBZM7n9EMwa0nK1yl0CA
L9-X4KASFfdhOeVeYSDgvA
yneTxW_9TTRXTOgJDH9fnQ
GGOH_X7npmcf3xYNtMeWcA
7GC9fVWKa4a1ZmBGLH6Uww
-F32Vl8Rk4dwsmk0f2wRIw
zSQps4R-_w8YkjDtgIsfiw
l81ILmOhky5bG7o4r3rkhQ
N1Q6HiZvnZHjNU712Gymqw
LMqKXdbwYdCqCCF64QbVkA
E5QyEU6FCQwnTys0S73zNw
3dPeTVuQatCgQeyJgkwKdA
KBpoIbLAQcEfMbmPIWFpiA
ST8Yzlk2MqKlcaLqL2djBg
IO3AsR6cdMto7VCwfPzf2w
v6CGBT0OoLRht9dzo7vaXg
Lp_Ykqfbv5Q-oyGYlMGJRg
eY9ZXESFPjhZf4rUFkssFQ
kJyR4gT1pfCcNjEY9-YMoQ
LqgGgWi3FLHBViX9tmZ9sw
--65q1FpAL_UQtVZ2PTGew
GuUQfQXqsN0MIGK4Lxvsjw
8JC-Yb3UDUv2FUl5ym1nVg
XeoAojoz5johV2MQ5ngNig
azj8vFl7JuSyHqamSVhd4A
palND-kF1qpMLhkcgAnSxA
-kIvLyWpY17aRa0vPp-RmA
wVSGZN8d3ao4ad97kEDzYg
X5GbNXY_nNoa_vTZDD0aCA
sDyaN_3DEZyhnJPUFIwoEg
VexAJmqOClKzm8KbY7xs5g
WGTEuxi9I5LBLjdUB7Pk_Q
yEQ96ibrgRxUaJP_wv5cbw
NfLyune1sAOVrHUAeQ9L-g
mECTORoeUYDA5ryP-vy5cw
hB0XY4B9ps6ALpBD2k_ZgQ
jdeNI5TTTuM6mj3HTgstRA
L9-X4KASFfdhOeVeYSDgvA
gv6GLZ3-bgSs44PtPJR1Bg
ZGfbxU-9wtRDTrfLRzfiMQ
wy8Yd_vCWDjiz9rMo4HfqA
cVcZifVh8iSVRso0pXhvBg
Ki71iAFTxsPPQfX430c99Q
wpqpfX_ueU6MH2_jlQgnkg
2AbBZM7n9EMwa0nK1yl0CA
yneTxW_9TTRXTOgJDH9fnQ
HestW1GKSkmUs_vpnauE_w
GGOH_X7npmcf3xYNtMeWcA
n-2gSytw4x3Q_rbweZnfuQ

User id: --0mI_q_0D1CdU4P_hoImQ
Depth: 1

results =
user_id

(Ο χρήστης --0mI_q_0D1CdU4P_hoImQ δεν επηρεάζει κανένα χρήστη στο ελάχιστο 
βάθος 1)

User id: n1KWJCpVeoTrzcN9iATfKA
Depth: 1

results =
user_id
XgIhw-aWaq_Fx3ZVQGjnuA


User id: n1KWJCpVeoTrzcN9iATfKA
Depth: 2

results = 
user_id

(Στην κονσόλα εμφανίζεται το μήνυμα: "User n1KWJCpVeoTrzcN9iATfKA doesn't affect 
any friends at depth 2 try using a lower depth value")




