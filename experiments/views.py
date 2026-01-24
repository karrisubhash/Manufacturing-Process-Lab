from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
import matplotlib.pyplot as plt
import io
import os
EXPERIMENTS = {
    "sieve-analysis": {
        "title": "Sieve Analysis – GFN",
        "slug": "sieve-analysis",
        "aim": "To determine the Grain Fineness Number of a given sand sample.",
        "procedure": [
            "Take 500g of sand.",
            "Put it through a series of sieves.",
            "Shake for 15 minutes.",
            "Weigh retained sand on each sieve.",
            "Calculate GFN using P×F method."
        ],
        "factors": [3, 10, 20, 40, 70, 140]
    },

    "moisture-content": {
        "title": "Moisture Content Test",
        "slug": "moisture-content",
        "aim": "To determine the percentage of moisture in a soil sample.",
        "procedure": [
            "Weigh the wet soil sample (W1).",
            "Dry the sample in an oven at 105°C for 24 hours.",
            "Weigh the dry sample (W2).",
            "Calculate Moisture Content = ((W1 - W2) / W2) × 100."
        ]
    },
     "clay-content": {
        "title": "Clay Content Test",
        "slug": "clay-content",
        "aim": "To determine the percentage of clay present in a given soil/sand sample.",
        "procedure": [
            "Take a known weight of soil sample (W1).",
            "Wash the sample over a 75-micron sieve until clear water passes.",
            "Dry the remaining soil in an oven at 105°C and weigh it (W2).",
            "Clay Content (%) = ((W1 - W2) / W1) × 100."
        ]
     },
     "green-compression": {
        "title": "Green Compression & Shear Strength Test",
        "slug": "green-compression",
        "aim": "To determine the Green Compressive Strength and shear strength of moulding sand using a Universal Strength Testing Machine.",
        "procedure": [
            "Prepare the sand specimen using a standard rammer and specimen tube.",
            "Place the specimen tube vertically with pedestal cup base.",
            "Place the specimen in the Universal Strength Testing Machine.",
            "Apply compressive load until the specimen fails.",
            "Note the compressive strength and shear strength readings from the machine.",
            "Repeat for 5 trials and calculate average values."
        ]
    },
    "single-v-butt": {
    "title": "Single V Butt Joint – Welding Experiment",
        "aim": "To study and perform the Single V Butt Joint welding.",
        "apparatus": [
            "Welding machine",
            "Mild steel plates",
            "Electrodes",
            "Welding table",
            "Protective gear (helmet, gloves, apron)"
        ],
        "procedure": [
            "Prepare two mild steel plates with beveled edges to form a V shape.",
            "Fix the plates properly on the welding table with a root gap.",
            "Switch on the welding machine and set the proper current.",
            "Strike the arc and begin welding from one end to the other.",
            "Maintain uniform speed and electrode angle during welding.",
            "Allow the joint to cool and clean the slag formed on the weld bead."
        ],
        "precautions": [
            "Always wear protective gear before starting the welding.",
            "Ensure proper earthing of the welding machine.",
            "Avoid looking at the arc without a protective shield.",
            "Keep inflammable materials away from the welding area.",
            "Do not touch hot metal immediately after welding."
        ],
        "reference_video": "https://www.youtube.com/embed/ttduOvHJiaY"  # replace with actual video ID
    
    },
     
# inside EXPERIMENTS = { ... }
"corner-joint": {
    "title": "Corner Joint Welding – Single Fillet",
    "slug": "corner-joint",
    "aim": "To prepare and inspect a single fillet corner joint and understand basic welding parameters.",
    "apparatus": [
        "Mild steel plates (specified size)",
        "Arc welding machine (or MIG/TIG as available)",
        "Electrodes suitable for material",
        "Electrode holder, ground clamp, chipping hammer",
        "Wire brush, files, measuring scale"
    ],
    "procedure": [
        "Clean the plate surfaces and remove rust/scale.",
        "Align the two plates at right angles (corner configuration) and tack-weld to hold.",
        "Set welding parameters (current, electrode, travel speed) according to electrode spec.",
        "Make the root pass, then finish with one or more filler passes to obtain a smooth fillet.",
        "Allow to cool, clean the weld and inspect for defects."
    ],
    "precautions": [
        "Always use proper PPE (welding helmet, gloves, apron).",
        "Ensure proper grounding and safe work area.",
        "Avoid flammable materials near the welding area.",
        "Do not touch hot metal after welding; allow to cool."
    ],
            "youtube_id": "https://www.youtube.com/embed/EI2t1Vyh8OY"  # replace with actual video ID

},
"double-parallel-fillet": {
    "title": "Double Parallel Fillet Joint Welding",
    "slug": "double-parallel-fillet",
    "aim": "To prepare and study a double parallel fillet joint and observe weld characteristics.",
    "apparatus": [
        "Mild steel plates (parallel configuration)",
        "Arc welding machine / MIG / TIG welder",
        "Electrodes suitable for base metal",
        "Electrode holder, ground clamp",
        "Chipping hammer, wire brush, safety PPE"
    ],
    "procedure": [
        "Clean the plate edges to remove rust, oil, or paint.",
        "Align the two plates in parallel lap configuration with suitable overlap.",
        "Tack weld at both ends to maintain alignment.",
        "Adjust welding current and electrode angle.",
        "Deposit fillet weld on one side, then weld on the opposite side for balance.",
        "Allow to cool, clean slag, and inspect the welds."
    ],
    "precautions": [
        "Wear proper PPE (helmet, gloves, apron).",
        "Ensure correct polarity and current settings.",
        "Keep electrodes dry and suitable for material.",
        "Avoid welding defects by maintaining steady travel speed."
    ],
    "youtube_id": "https://www.youtube.com/embed/tXKiEVr_K6w"   # put your YouTube video ID here
},
"solid-flange": {
    "title": "Mould Cavity for Solid Flange",
    "slug": "solid-flange",
    "aim": "To prepare sand using the given single piece pattern for a solid flange.",
    "apparatus": [
        "Moulding board",
        "Cope and drag boxes",
        "Moulding sand",
        "Parting sand",
        "Rammer",
        "Strike-off bar",
        "Bellows and riser",
        "Sprue pins",
        "Gate cutter",
        "Vent rod",
        "Draw spike"
    ],
    "procedure": [
        "The pattern is placed on molding board with its flat side on the board.",
        "The drag box is placed over the board, after giving its clay wash inside.",
        "Parting sand is sprinkled over the pattern and molding board.",
        "Foundry sand is placed over the pattern and it is covered to a depth of 20 to 30 mm.",
        "Using fingers sand is packed around the pattern and into the corners of the box with rammer.",
        "Excess sand is struck off with strike-off bar.",
        "The drag is turned upside down.",
        "Sand particles are blown off with bellows and surface is smoothened.",
        "Cope box is placed on drag after giving clay wash inside.",
        "Riser pin is placed on pattern, sprue pin placed on opposite side.",
        "Parting sand is sprinkled on upper surface.",
        "Steps 4 to 7 are repeated.",
        "Vent holes are made with vent rod about 10 mm from pattern.",
        "Sprue and riser pins removed carefully, leaving pouring basin and cup.",
        "Cope is lifted and placed aside.",
        "Pattern is drawn out using draw spike carefully.",
        "Mold is prepared by adding sand where defective.",
        "Loose sand blown off.",
        "Cope is replaced and weights placed on top."
    ],
    "precautions": [
        "Add sufficient amount of water till the sand attains sufficient strength.",
        "Ramming should be done uniformly.",
        "Proper care should be taken while removing the pattern without broken edges."
    ],
    "result": "The sand mold for a solid flange is thus made and is ready for pouring the molten metal."
},

"solid-flange": {
    "title": "Mould Cavity for Solid Flange",
    "slug": "solid-flange",
    "aim": "To prepare sand using the given single piece pattern for a solid flange.",
    "apparatus": [
        "Moulding board",
        "Cope and drag boxes",
        "Moulding sand",
        "Parting sand",
        "Rammer",
        "Strike-off bar",
        "Bellows and riser",
        "Sprue pins",
        "Gate cutter",
        "Vent rod",
        "Draw spike"
    ],
    "procedure": [
        "The pattern is placed on molding board with its flat side on the board.",
        "The drag box is placed over the board, after giving its clay wash inside.",
        "Parting sand is sprinkled over the pattern and molding board.",
        "Foundry sand is placed over the pattern and it is covered to a depth of 20 to 30 mm.",
        "Using fingers sand is packed around the pattern and into the corners of the box with rammer.",
        "Excess sand is struck off with strike-off bar.",
        "The drag is turned upside down.",
        "Sand particles are blown off with bellows and surface is smoothened.",
        "Cope box is placed on drag after giving clay wash inside.",
        "Riser pin is placed on pattern, sprue pin placed on opposite side.",
        "Parting sand is sprinkled on upper surface.",
        "Steps 4 to 7 are repeated.",
        "Vent holes are made with vent rod about 10 mm from pattern.",
        "Sprue and riser pins removed carefully, leaving pouring basin and cup.",
        "Cope is lifted and placed aside.",
        "Pattern is drawn out using draw spike carefully.",
        "Mold is prepared by adding sand where defective.",
        "Loose sand blown off.",
        "Cope is replaced and weights placed on top."
    ],
    "precautions": [
        "Add sufficient amount of water till the sand attains sufficient strength.",
        "Ramming should be done uniformly.",
        "Proper care should be taken while removing the pattern without broken edges."
    ],
    "result": "The sand mold for a solid flange is thus made and is ready for pouring the molten metal."
},

"Stepped-cone": {
    "title": "Mould Cavity for Stepped Cone Pulley",
    "slug": "Stepped-cone",
    "aim": "To prepare sand mould,using the given split pattern for a stepped cone pulley.",
    "apparatus": [
        "Moulding board",
        "Cope and drag boxes",
        "Moulding sand",
        "Parting sand",
        "Rammer",
        "Strike-off bar",
        "Bellows and riser",
        "Sprue pins",
        "Gate cutter",
        "Vent rod",
        "Draw spike"
    ],
    "procedure": [
        "The pattern is placed on molding board with its flat side on the board.",
        "The drag box is placed over the board, after giving its clay wash inside.",
        "Parting sand is sprinkled over the pattern and molding board.",
        "Foundry sand is placed over the pattern and it is covered to a depth of 20 to 30 mm.",
        "Using fingers sand is packed around the pattern and into the corners of the box with rammer.",
        "Excess sand is struck off with strike-off bar.",
        "The drag is turned upside down.",
        "Sand particles are blown off with bellows and surface is smoothened.",
        "Cope box is placed on drag after giving clay wash inside.",
        "Riser pin is placed on pattern, sprue pin placed on opposite side.",
        "Parting sand is sprinkled on upper surface.",
        "Steps 4 to 7 are repeated.",
        "Vent holes are made with vent rod about 10 mm from pattern.",
        "Sprue and riser pins removed carefully, leaving pouring basin and cup.",
        "Cope is lifted and placed aside.",
        "Pattern is drawn out using draw spike carefully.",
        "Mold is prepared by adding sand where defective.",
        "Loose sand blown off.",
        "Cope is replaced and weights placed on top."
    ],
    "precautions": [
        "Add sufficient amount of water till the sand attains sufficient strength.",
        "Ramming should be done uniformly.",
        "Proper care should be taken while removing the pattern without broken edges."
    ],
    "result": "The sand mold for a stepped cone pulley is thus made and is ready for pouring the molten metal."
},
"Hollow-pipe": {
    "title": "Mould Cavity for Hollow Pipe Single Pattern",
    "slug": "Hollow-pipe",
    "aim": "To prepare sand mould,using the given split pattern for a Hollow Pipe Single Pattern.",
    "apparatus": [
        "Moulding board",
        "Cope and drag boxes",
        "Moulding sand",
        "Parting sand",
        "Rammer",
        "Strike-off bar",
        "Bellows and riser",
        "Sprue pins",
        "Gate cutter",
        "Vent rod",
        "Draw spike"
    ],
    "procedure": [
        "The pattern is placed on molding board with its flat side on the board.",
        "The drag box is placed over the board, after giving its clay wash inside.",
        "Parting sand is sprinkled over the pattern and molding board.",
        "Foundry sand is placed over the pattern and it is covered to a depth of 20 to 30 mm.",
        "Using fingers sand is packed around the pattern and into the corners of the box with rammer.",
        "Excess sand is struck off with strike-off bar.",
        "The drag is turned upside down.",
        "Sand particles are blown off with bellows and surface is smoothened.",
        "Cope box is placed on drag after giving clay wash inside.",
        "Riser pin is placed on pattern, sprue pin placed on opposite side.",
        "Parting sand is sprinkled on upper surface.",
        "Steps 4 to 7 are repeated.",
        "Vent holes are made with vent rod about 10 mm from pattern.",
        "Sprue and riser pins removed carefully, leaving pouring basin and cup.",
        "Cope is lifted and placed aside.",
        "Pattern is drawn out using draw spike carefully.",
        "Mold is prepared by adding sand where defective.",
        "Loose sand blown off.",
        "Cope is replaced and weights placed on top."
    ],
    "precautions": [
        "Add sufficient amount of water till the sand attains sufficient strength.",
        "Ramming should be done uniformly.",
        "Proper care should be taken while removing the pattern without broken edges."
    ],
    "result": "The sand mold for a Hollow Pipe Single Pattern is thus made and is ready for pouring the molten metal."
}


}


def experiment_list(request):
    return render(request, 'experiments/experiment_list.html', {'experiments': EXPERIMENTS})

def run_experiment(request, slug):
    experiment = EXPERIMENTS.get(slug)
    if not experiment:
        return HttpResponse("Experiment not found", status=404)

    result = None
    steps = ""
    weights = []
    graph_data = {}
    weight_inputs = [""] * 6
    email = ""
    moisture_results=[]
    W1=""
    W2=""
    clay_content=""
    result_gc=None
    result_shear=None
    gc_values=""
    steps_shear=[]
    
    trials = [{'trial': i, 'gc': '', 'shear': ''} for i in range(1, 6)]

    
    NUM_MOISTURE_SAMPLES = 5
    moisture_results = [
        {"sample": i, "W1": "", "W2": "", "mc": ""} for i in range(1, NUM_MOISTURE_SAMPLES + 1)
    ]
    context=[]
    dims = []
    steps_html = "" 
    table_html = ""
    email_sent = False

    if slug=='sieve-analysis':
        template = 'experiments/experiment_run.html'
    
    elif slug == "moisture-content":
        template = 'experiments/moisture_content.html'
    elif slug=="clay-content":
        template='experiments/clay_content.html'
    
    elif slug =="green-compression":
        template='experiments/green_compression.html'
    elif slug=="single-v-butt":
         template = 'experiments/single_v_butt.html'
    elif slug=="corner-joint":
                 template = 'experiments/corner_joint.html'
    elif slug == 'double-parallel-fillet':
         template = 'experiments/double_parallel_fillet.html'
    elif slug=='solid-flange':
        template='experiments/solid_flange.html'
    elif slug=='Stepped-cone':
        template='experiments/stepped_cone.html'
    elif slug=='Hollow-pipe':
        template='experiments/Hollow_pipe.html'

        
        

    if request.method == "POST":
        email = request.POST.get("email", "")
        from_result = request.POST.get("from_result", "") == "true"

        try:
            #sieve-analysis
            if slug == "sieve-analysis":
                weight_inputs = [request.POST.get(f'w{i}', "") for i in range(1, 7)]
                weights = [float(w) if w else 0.0 for w in weight_inputs]
                total_weight = sum(weights)

                if total_weight == 0:
                    steps = "<span style='color:red;'>Total weight is zero. Please enter valid weights.</span>"
                else:
                    factors = experiment["factors"]
                    p_values = [(w / total_weight) * 100 for w in weights]
                    pf_values = [round(p * f, 2) for p, f in zip(p_values, factors)]
                    total_pf = round(sum(pf_values), 2)
                    gfn = round(total_pf / 100, 2)
                    result = gfn

                    steps += "<strong>Formula:</strong><br>"
                    steps += "P(%) = (Weight Retained / Total Weight) × 100<br>"
                    steps += "P × F = P% × Sieve Factor<br><br>"
                    steps += f"<strong>Step-by-Step Calculations:</strong><br>Total Weight = {total_weight}g<br><br>"
                    steps += f"Total Weight = {total_weight}g<br><br>"

                    email_subject = "Sieve Analysis Result – GFN"
                    email_html_message = """
                    <h2>Observation Table</h2>
                    <table border="1" cellpadding="6" cellspacing="0">
                        <tr><th>Sieve No.</th><th>Weight (g)</th><th>P (%)</th><th>P × F</th></tr>
                    """

                    for i in range(6):
                        w = weights[i]
                        f = factors[i]
                        p = round(p_values[i], 2)
                        pf = pf_values[i]
                        steps += f"Sieve No. {f}:<br>- Weight Retained = {w}g<br>- P(%) = {p}%<br>- P × F = {pf}<br><br>"

                        steps += f"Sieve No. {f}: {w}g → P={p}% → P×F={pf}<br><br>"
                        email_html_message += f"<tr><td>{f}</td><td>{w}</td><td>{p}</td><td>{pf}</td></tr>"

                    steps += f"<strong>Σ(P × F) = {total_pf}</strong><br>"
                    steps += f"<strong>GFN = Σ(P × F) / 100 = {total_pf} / 100 = <span style='color:green;'>{gfn}</span></strong><br>"
                    email_html_message += "</table><br><h2>Calculation Explanation</h2>"
                    email_html_message += f"<p>Total Weight = {total_weight}g</p>"

                    for i in range(6):
                        w = weights[i]
                        f = factors[i]
                        p = round(p_values[i], 2)
                        pf = pf_values[i]
                        email_html_message += f"""
                        <p><strong>Sieve {f}:</strong><br>
                        Weight Retained = {w}g<br>
                        P(%) = ({w} / {total_weight}) × 100 = {p}%<br>
                        P × F = {p} × {f} = {pf}</p>
                        """

                    email_html_message += f"""
                    <p><strong>Σ(P × F) = {total_pf}</strong><br>
                    <strong>GFN = {gfn}</strong></p>
                    <h2>Graph:</h2>
                    <img src="cid:graph_inline"><br><br>
                    Regards,<br>Designed by Subhash
                    """
                    # Graph
                    graph_data = {'sieves': factors, 'percentages': [round(p, 2) for p in p_values]}
                    buf = io.BytesIO()
                    plt.figure(figsize=(6, 4))
                    plt.plot(factors, graph_data['percentages'], marker='o', linestyle='-', color='blue')
                    plt.xlabel('Sieve No.')
                    plt.ylabel('P (%)')
                    plt.title('Sieve Analysis Graph')
                    plt.grid(True)
                    plt.tight_layout()
                    plt.savefig(buf, format='png')
                    buf.seek(0)
                    plt.close()
                    if email and result and from_result:
                        msg = EmailMultiAlternatives(
                            subject=email_subject,
                            body="Please view this email in HTML mode.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[email],
                        )
                        msg.attach_alternative(email_html_message, "text/html")

                        image = MIMEImage(buf.read(), _subtype="png")
                        image.add_header('Content-ID', '<graph_inline>')
                        image.add_header("Content-Disposition", "inline", filename="graph.png")
                        msg.attach(image)

                        msg.send()
                    steps += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"

                    
                        # ----------------------------
             # ---------- MOISTURE CONTENT (5 samples) ----------
            elif slug == "moisture-content":
                mc_values = []        # numeric MC (valid samples)
                lines = []            # step lines (HTML)
                lines.append("<strong>Formula:</strong><br>Moisture (%) = ((W1 - W2) / W2) × 100<br><br>")
                lines.append("<strong>Step-by-step for each sample:</strong><br>")

                moisture_results = []  # will re-build with posted values and mc
                for i in range(1, 6):  # 1..5
                    raw_w1 = request.POST.get(f"W1_{i}", "").strip()
                    raw_w2 = request.POST.get(f"W2_{i}", "").strip()

                    # default display strings (so template pre-fills)
                    display_w1 = raw_w1
                    display_w2 = raw_w2
                    mc_display = ""

                    # if user didn't enter either, skip
                    if raw_w1 == "" and raw_w2 == "":
                        lines.append(f"Sample {i}: no data provided; skipped.<br>")
                        moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})
                        continue

                    # try parse floats
                    try:
                        W1 = float(raw_w1) if raw_w1 != "" else None
                        W2 = float(raw_w2) if raw_w2 != "" else None
                    except ValueError:
                        lines.append(f"Sample {i}: invalid numeric input (W1='{raw_w1}', W2='{raw_w2}'); skipped.<br>")
                        moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})
                        continue

                    if W1 is None or W2 is None:
                        lines.append(f"Sample {i}: missing W1 or W2; skipped.<br>")
                        moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})
                        continue

                    # logical checks
                    if W2 <= 0:
                        lines.append(f"Sample {i}: invalid W2 (must be > 0). Given W2={W2}; skipped.<br>")
                        moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})
                        continue
                    if W1 <= W2:
                        lines.append(f"Sample {i}: invalid (W1 must be > W2). Given W1={W1}, W2={W2}; skipped.<br>")
                        moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})
                        continue

                    # compute
                    diff = W1 - W2
                    ratio = diff / W2
                    mc_value = round(ratio * 100, 2)   # percent rounded to 2 dp
                    mc_values.append(mc_value)
                    mc_display = mc_value

                    # build a clear step line with intermediate values
                    lines.append(
                        (f"<strong>Sample {i}:</strong> W1 = {W1:.2f} g, W2 = {W2:.2f} g → "
                         f"W1 - W2 = {diff:.2f} g → ({diff:.2f} / {W2:.2f}) = {ratio:.6f} → "
                         f"{ratio:.6f} × 100 = {ratio * 100:.6f} % → <em>Rounded:</em> {mc_value:.2f} %<br>")
                    )

                    moisture_results.append({"sample": i, "W1": display_w1, "W2": display_w2, "mc": mc_display})

                # final average (only valid mc_values)
                if mc_values:
                    avg_mc = round(sum(mc_values) / len(mc_values), 2)
                    result = f"{avg_mc} %"
                    lines.append(f"<br><strong>Average Moisture Content (over {len(mc_values)} sample(s)) = {avg_mc} %</strong><br>")
                else:
                    lines.append("<br><span style='color:red;'><strong>No valid samples were provided to compute an average.</strong></span><br>")

                steps = "".join(lines)
                                # optional email sending (HTML table + steps)
                if email and result and from_result:
                    try:
                        email_subject = "Moisture Content Test Results"
                        html_table = """
                        <h3>Moisture Content Results</h3>
                        <table border='1' cellpadding='6' cellspacing='0' style='border-collapse: collapse;'>
                            <tr style='background:#f0f0f0;'>
                                <th>Sample</th>
                                <th>Wet Weight (W1)</th>
                                <th>Dry Weight (W2)</th>
                                <th>Moisture (%)</th>
                            </tr>
                        """
                        for r in moisture_results:
                            html_table += f"<tr><td>{r['sample']}</td><td>{r['W1']}</td><td>{r['W2']}</td><td>{r['mc']}</td></tr>"
                        html_table += "</table>"

                        # add average + step-by-step explanation
                        html_body = f"""
                        <html>
                        <body>
                            {html_table}
                            <br>
                            <h4>Average Moisture Content:</h4>
                            <p><strong>{result}</strong></p>
                            <hr>
                            <h4>Step-by-Step Calculation:</h4>
                            {steps}
                            <br><br>
                            <p>Regards,<br>Designed By Subhash</p>
                        </body>
                        </html>
                        """

                        msg = EmailMultiAlternatives(
                            subject=email_subject,
                            body="Please view this email in HTML mode.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[email],
                        )
                        msg.attach_alternative(html_body, "text/html")
                        msg.send()

                        steps += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"
                    except Exception as e:
                        steps += f"<div class='alert alert-warning mt-3'>Email sending failed: {e}</div>"

            elif slug == "clay-content":
                W1 = float(request.POST.get("W1", 0))
                W2 = float(request.POST.get("W2", 0))

                if W1 <= 0 or W2 <= 0 or W1 <= W2:
                    steps = "<span style='color:red;'>Please enter valid values (W1 > W2 > 0).</span>"
                else:
                    clay_content = round(((W1 - W2) / W1) * 100, 2)
                    result = f"{clay_content} %"
                    steps = f"""
                        <strong>Formula:</strong><br>
                        Clay Content = ((W1 - W2) / W1) × 100<br><br>
                        <strong>Step-by-Step:</strong><br>
                        W1 (Initial weight) = {W1} g<br>
                        W2 (Final weight) = {W2} g<br>
                        Clay Content = (({W1} - {W2}) / {W1}) × 100 = {clay_content} %
                    """

                    email_subject = "Clay Content Test Result"
                    email_html_message = f"""
                    <h2>Clay Content Test Result</h2>
                    <p><strong>Formula:</strong> Clay Content = ((W1 - W2) / W1) × 100</p>
                    <h3>Step-by-Step-Calculation:</h3>
                    <ul>
                    <li>W1 (Initial weight) = {W1} g</li>
                    <li>W2 (Final weight) = {W2} g</li>
                    <li>Clay Content = (({W1} - {W2}) / {W1}) × 100 = <b>{clay_content} %</b></li>
                    </ul>
                    <hr>
                    <p><b>Final Result:</b> {clay_content} %</p>
                    <p>Regards,<br>Designed by Subhash</p>
                    """

                    if email and result and from_result:
                        msg = EmailMultiAlternatives(
                            subject=email_subject,
                            body="Please view this email in HTML mode.",
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            to=[email],
                        )
                        msg.attach_alternative(email_html_message, "text/html")
                        msg.send()
                        steps += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"
             
            elif slug == "green-compression":
               
                gc_values = []
                shear_values = []
                steps_gc = []
                steps_shear = []
                trials = []  # reset and refill with user inputs

                for i in range(1, 6):
                    raw_gc = request.POST.get(f'GC{i}', '').strip()
                    raw_shear = request.POST.get(f'Shear{i}', '').strip()

                    trial_data = {'trial': i, 'gc': raw_gc, 'shear': raw_shear}

                    # Green Compression
                    if raw_gc:
                        try:
                            v = float(raw_gc)
                            gc_values.append(v)
                            steps_gc.append(f"Trial {i}: GC = {v:.2f}")
                        except:
                            pass

                    # Shear Strength
                    if raw_shear:
                        try:
                            v = float(raw_shear)
                            shear_values.append(v)
                            steps_shear.append(f"Trial {i}: Shear = {v:.2f}")
                        except:
                            pass

                    trials.append(trial_data)

                # Calculate Green Compression average
                if gc_values:
                    total_gc = sum(gc_values)
                    avg_gc = total_gc / len(gc_values)
                    result_gc = f"{avg_gc:.2f}"
                    steps += "<h4>Green Compression Strength</h4><ul>"
                    for line in steps_gc:
                        steps += f"<li>{line}</li>"
                    steps += f"</ul><p>Σ(GC) = {total_gc:.2f},<br> →No of trials = {len(gc_values)}  <br>→Average = {avg_gc:.2f}</p>"

                # Calculate Shear Strength average
                if shear_values:
                    total_shear = sum(shear_values)
                    avg_shear = total_shear / len(shear_values)
                    result_shear = f"{avg_shear:.2f}"
                    steps += "<h4>Shear Strength</h4><ul>"
                    for line in steps_shear:
                        steps += f"<li>{line}</li>"
                    steps += f"</ul><p>Σ(Shear) = {total_shear:.2f}, <br>→No of trials = {len(shear_values)} <br>→ Average = {avg_shear:.2f}</p>"

                if not gc_values and not shear_values:
                    steps = "<div class='text-danger'>No valid values entered.</div>"
                if email and from_result and (result_gc or result_shear):
                        email_subject = "Green Compression & Shear Strength Results"
                        email_html_message = """
                        <h2>Observation Table</h2>
                        <table border="1" cellpadding="6" cellspacing="0">
                            <tr><th>Trial</th><th>Green Compression</th><th>Shear Strength</th></tr>
                        """
                        for t in trials:
                            email_html_message += f"<tr><td>{t['trial']}</td><td>{t['gc']}</td><td>{t['shear']}</td></tr>"
                        email_html_message += "</table><br>"

                        # Step by step calculations
                        if gc_values:
                            email_html_message += "<h3>Green Compression Strength Calculations</h3><ul>"
                            for line in steps_gc:
                                email_html_message += f"<li>{line}</li>"
                            total_gc = sum(gc_values)
                            avg_gc = total_gc / len(gc_values)
                            email_html_message += f"</ul><p>Σ(GC) = {total_gc:.2f}, <br>→ No of trials = {len(gc_values)}<br> → Average = <b>{avg_gc:.2f}</b></p>"

                        if shear_values:
                            email_html_message += "<h3>Shear Strength Calculations</h3><ul>"
                            for line in steps_shear:
                                email_html_message += f"<li>{line}</li>"
                            total_shear = sum(shear_values)
                            avg_shear = total_shear / len(shear_values)
                            email_html_message += f"</ul><p>Σ(Shear) = {total_shear:.2f},<br>→ No of trials = {len(shear_values)}<br> → Average = <b>{avg_shear:.2f}</b></p>"

                        email_html_message += "<br><p>Regards,<br>Designed by Subhash</p>"

                        try:
                            msg = EmailMultiAlternatives(
                                subject=email_subject,
                                body="Please view this email in HTML mode.",
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                to=[email],
                            )
                            msg.attach_alternative(email_html_message, "text/html")
                            msg.send()
                            steps += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"
                        except Exception as e:
                            steps += f"<div class='text-danger'>Error sending email: {e}</div>"
             
           
            elif slug == "single-v-butt":
                template = "experiments/single_v_butt.html"
            elif slug=="corner-joint":
                         template = 'corner_joint.html'
            elif slug == 'double-parallel-fillet':
                 template = 'experiments/double_parallel_fillet.html'
            
            elif slug == 'solid-flange':
                template = 'experiments/solid_flange.html'
                dims = []
                steps_html = ""
                table_html = ""
                email_sent = False

                if request.method == "POST":
                    # Check if this request is for sending email only
                    if "send_email" in request.POST:
                        # Retrieve saved calculation results from the session
                        table_html = request.session.get("solid_flange_table", "")
                        steps_html = request.session.get("solid_flange_steps", "")
                        dims = request.session.get("solid_flange_dims", [])
                        email = request.POST.get("email", "").strip()

                        if email and table_html:
                            subject = "Solid Flange Experiment Results"
                            msg = EmailMultiAlternatives(
                                subject,
                                "Please view this email in HTML mode.",
                                settings.DEFAULT_FROM_EMAIL,
                                [email]
                            )
                            full_html = f"""
                            <html><body>
                            {table_html}
                            <br><h4>Step-by-Step Calculations:</h4>
                            {steps_html}
                            </body></html>
                            """
                            msg.attach_alternative(full_html, "text/html")
                            msg.send()
                            email_sent = True
                            steps_html += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"


                    else:
                        # Perform calculation
                        for i in range(1, 4):
                            raw_cast = request.POST.get(f"casting_{i}", "").strip()
                            raw_shrink = request.POST.get(f"shrinkage_{i}", "").strip()
                            raw_mach = request.POST.get(f"machining_{i}", "").strip()

                            if raw_cast == "" and raw_shrink == "" and raw_mach == "":
                                continue

                            try:
                                casting = float(raw_cast)
                                shrink_pct = float(raw_shrink)
                                machining = float(raw_mach)

                                after_shrink = casting / (1 + shrink_pct / 100.0)
                                final_dim = after_shrink - machining

                                dims.append({
                                    "index": i,
                                    "casting": casting,
                                    "shrink_pct": shrink_pct,
                                    "after_shrink": after_shrink,
                                    "machining": machining,
                                    "final_raw": final_dim,
                                    "final_rounded": round(final_dim, 2),
                                })

                                steps_html += f"""
                                <div class="mb-3">
                                    <strong>Dimension {i}:</strong><br>
                                    Pattern Dimension = {casting} mm<br>
                                    Shrinkage Allowance = {shrink_pct}%<br>
                                    After Shrinkage = {casting} / (1 + {shrink_pct}/100) = {after_shrink:.2f} mm<br>
                                    Machining Allowance = {machining} mm<br>
                                    Final Dimension = {after_shrink:.2f} - {machining} = {final_dim:.2f} mm<br>
                                    <em>Rounded: {round(final_dim, 2)} mm</em>
                                </div>
                                """
                            except Exception as e:
                                steps_html += f"<p><strong>Dimension {i}:</strong> Error - {e}</p>"

                        # ✅ Build result table (for display and email)
                        if dims:
                            table_html = """
                            <h3>Solid Flange Experiment Results</h3>
                            <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
                            <tr>
                                <th>Dimension</th>
                                <th>Casting (mm)</th>
                                <th>Shrinkage (%)</th>
                                <th>After Shrinkage (mm)</th>
                                <th>Machining (mm)</th>
                                <th>Final Dimension (mm)</th>
                            </tr>
                            """
                            for d in dims:
                                table_html += f"""
                                <tr>
                                    <td>{d['index']}</td>
                                    <td>{d['casting']}</td>
                                    <td>{d['shrink_pct']}</td>
                                    <td>{d['after_shrink']:.2f}</td>
                                    <td>{d['machining']}</td>
                                    <td><b>{d['final_rounded']}</b></td>
                                </tr>
                                """
                            table_html += "</table>"

                        # ✅ Save to session so we can send via email later
                        request.session["solid_flange_table"] = table_html
                        request.session["solid_flange_steps"] = steps_html
                        request.session["solid_flange_dims"] = dims

                # Return context
                context = {
                    'experiment': experiment,
                    'dims': dims,
                    'steps': steps_html,
                    'email_sent': email_sent,
                    'casting_1': request.POST.get("casting_1", ""),
                    'casting_2': request.POST.get("casting_2", ""),
                    'casting_3': request.POST.get("casting_3", ""),
                    'shrinkage_1': request.POST.get("shrinkage_1", ""),
                    'shrinkage_2': request.POST.get("shrinkage_2", ""),
                    'shrinkage_3': request.POST.get("shrinkage_3", ""),
                    'machining_1': request.POST.get("machining_1", ""),
                    'machining_2': request.POST.get("machining_2", ""),
                    'machining_3': request.POST.get("machining_3", ""),
                }
                return render(request, template, context)
            elif slug == 'Stepped-cone':
                template = 'experiments/stepped_cone.html'
                dims = []
                steps_html = ""
                table_html = ""
                email_sent = False

                if request.method == "POST":
                    # Check if this request is for sending email only
                    if "send_email" in request.POST:
                        # Retrieve saved calculation results from the session
                        table_html = request.session.get("stepped_cone_table", "")
                        steps_html = request.session.get("stepped_cone_steps", "")
                        dims = request.session.get("stepped_cone_dims", [])
                        email = request.POST.get("email", "").strip()

                        if email and table_html:
                            subject = "Stepped cone Experiment Results"
                            msg = EmailMultiAlternatives(
                                subject,
                                "Please view this email in HTML mode.",
                                settings.DEFAULT_FROM_EMAIL,
                                [email]
                            )
                            full_html = f"""
                            <html><body>
                            {table_html}
                            <br><h4>Step-by-Step Calculations:</h4>
                            {steps_html}
                            </body></html>
                            """
                            msg.attach_alternative(full_html, "text/html")
                            msg.send()
                            email_sent = True
                            steps_html += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"
                            
 
                    else:
                        for i in range(1, 5):  # 4 dimensions
                            raw_cast = request.POST.get(f"casting_{i}", "").strip()
                            raw_shrink = request.POST.get(f"shrinkage_{i}", "").strip()
                            raw_mach = request.POST.get(f"machining_{i}", "").strip()

                            if raw_cast == "" and raw_shrink == "" and raw_mach == "":
                                continue

                            try:
                                casting = float(raw_cast)
                                shrink_pct = float(raw_shrink)
                                machining = float(raw_mach)

                                after_shrink = casting / (1 + shrink_pct / 100.0)
                                final_dim = after_shrink - machining

                                dims.append({
                                    "index": i,
                                    "casting": casting,
                                    "shrink_pct": shrink_pct,
                                    "after_shrink": after_shrink,
                                    "machining": machining,
                                    "final_raw": final_dim,
                                    "final_rounded": round(final_dim, 2),
                                })

                                steps_html += f"""
                                <div class="mb-3">
                                    <strong>Dimension {i}:</strong><br>
                                    Pattern Dimension = {casting} mm<br>
                                    Shrinkage Allowance = {shrink_pct}%<br>
                                    After Shrinkage = {casting} / (1 + {shrink_pct}/100) = {after_shrink:.2f} mm<br>
                                    Machining Allowance = {machining} mm<br>
                                    Final Dimension = {after_shrink:.2f} - {machining} = {final_dim:.2f} mm<br>
                                    <em>Rounded: {round(final_dim, 2)} mm</em>
                                </div>
                                """

                            except Exception as e:
                                steps_html += f"<p><strong>Dimension {i}:</strong> Error - {e}</p>"

                    # ✅ Build email table after loop
                    if dims:
                        table_html = """
                        <h3>Mould for Stepped Cone Pulley - Experiment Results</h3>
                        <table border="1" cellpadding="6" cellspacing="0">
                        <tr>
                            <th>Dimension</th>
                            <th>Pattern (mm)</th>
                            <th>Shrinkage (%)</th>
                            <th>After Shrinkage (mm)</th>
                            <th>Machining (mm)</th>
                            <th>Casting (mm)</th>
                        </tr>
                        """
                        for d in dims:
                            table_html += f"""
                            <tr>
                                <td>{d['index']}</td>
                                <td>{d['casting']}</td>
                                <td>{d['shrink_pct']}</td>
                                <td>{d['after_shrink']:.2f}</td>
                                <td>{d['machining']}</td>
                                <td><b>{d['final_rounded']}</b></td>
                            </tr>
                            """
                        table_html+="</table>"
                    # ✅ Save to session so we can send via email later
                    request.session["stepped_cone_table"] = table_html
                    request.session["stepped_cone_steps"] = steps_html
                    request.session["stepped_cone_dims"] = dims


                context = {
                    'experiment': experiment,
                    'dims': dims,
                    'steps': steps_html,
                    'email_sent': email_sent,
                    'casting_1': request.POST.get("casting_1", ""),
                    'casting_2': request.POST.get("casting_2", ""),
                    'casting_3': request.POST.get("casting_3", ""),
                    'casting_4': request.POST.get("casting_4", ""),
                    'shrinkage_1': request.POST.get("shrinkage_1", ""),
                    'shrinkage_2': request.POST.get("shrinkage_2", ""),
                    'shrinkage_4': request.POST.get("shrinkage_4", ""),
                    'shrinkage_3': request.POST.get("shrinkage_3", ""),
                    'machining_1': request.POST.get("machining_1", ""),
                    'machining_2': request.POST.get("machining_2", ""),
                    'machining_3': request.POST.get("machining_3", ""),
                    'machining_4': request.POST.get("machining_4", ""),
                }


        
                return render(request, template, context)
            elif slug=='Hollow-pipe':
                 template='experiments/Hollow_pipe.html'
                 dims = []
                 steps_html = ""
                 table_html = ""
                 email_sent = False

                 if request.method == "POST":
                    # Check if this request is for sending email only
                    if "send_email" in request.POST:
                        # Retrieve saved calculation results from the session
                        table_html = request.session.get("solid_flange_table", "")
                        steps_html = request.session.get("solid_flange_steps", "")
                        dims = request.session.get("solid_flange_dims", [])
                        email = request.POST.get("email", "").strip()

                        if email and table_html:
                            subject = "Hollow Pipe- Experiment Results"
                            msg = EmailMultiAlternatives(
                                subject,
                                "Please view this email in HTML mode.",
                                settings.DEFAULT_FROM_EMAIL,
                                [email]
                            )
                            full_html = f"""
                            <html><body>
                            {table_html}
                            <br><h4>Step-by-Step Calculations:</h4>
                            {steps_html}
                            </body></html>
                            """
                            msg.attach_alternative(full_html, "text/html")
                            msg.send()
                            email_sent = True
                            steps_html += f"<div class='alert alert-info mt-3'>Result sent to <strong>{email}</strong></div>"


                    else:
                        # Perform calculation
                        for i in range(1, 4):
                            raw_cast = request.POST.get(f"casting_{i}", "").strip()
                            raw_shrink = request.POST.get(f"shrinkage_{i}", "").strip()
                            raw_mach = request.POST.get(f"machining_{i}", "").strip()

                            if raw_cast == "" and raw_shrink == "" and raw_mach == "":
                                continue

                            try:
                                casting = float(raw_cast)
                                shrink_pct = float(raw_shrink)
                                machining = float(raw_mach)

                                after_shrink = casting / (1 + shrink_pct / 100.0)
                                final_dim = after_shrink - machining

                                dims.append({
                                    "index": i,
                                    "casting": casting,
                                    "shrink_pct": shrink_pct,
                                    "after_shrink": after_shrink,
                                    "machining": machining,
                                    "final_raw": final_dim,
                                    "final_rounded": round(final_dim, 2),
                                })

                                steps_html += f"""
                                <div class="mb-3">
                                    <strong>Dimension {i}:</strong><br>
                                    Pattern Dimension = {casting} mm<br>
                                    Shrinkage Allowance = {shrink_pct}%<br>
                                    After Shrinkage = {casting} / (1 + {shrink_pct}/100) = {after_shrink:.2f} mm<br>
                                    Machining Allowance = {machining} mm<br>
                                    Final Dimension = {after_shrink:.2f} - {machining} = {final_dim:.2f} mm<br>
                                    <em>Rounded: {round(final_dim, 2)} mm</em>
                                </div>
                                """
                            except Exception as e:
                                steps_html += f"<p><strong>Dimension {i}:</strong> Error - {e}</p>"

                        # ✅ Build result table (for display and email)
                        if dims:
                            table_html = """
                            <h3>Hollow Pipe Experiment Results</h3>
                            <table border="1" cellpadding="6" cellspacing="0" style="border-collapse: collapse;">
                            <tr>
                                <th>Dimension</th>
                                <th>Casting (mm)</th>
                                <th>Shrinkage (%)</th>
                                <th>After Shrinkage (mm)</th>
                                <th>Machining (mm)</th>
                                <th>Final Dimension (mm)</th>
                            </tr>
                            """
                            for d in dims:
                                table_html += f"""
                                <tr>
                                    <td>{d['index']}</td>
                                    <td>{d['casting']}</td>
                                    <td>{d['shrink_pct']}</td>
                                    <td>{d['after_shrink']:.2f}</td>
                                    <td>{d['machining']}</td>
                                    <td><b>{d['final_rounded']}</b></td>
                                </tr>
                                """
                            table_html += "</table>"

                        # ✅ Save to session so we can send via email later
                        request.session["solid_flange_table"] = table_html
                        request.session["solid_flange_steps"] = steps_html
                        request.session["solid_flange_dims"] = dims

                # Return context
                 context = {
                    'experiment': experiment,
                    'dims': dims,
                    'steps': steps_html,
                    'email_sent': email_sent,
                    'casting_1': request.POST.get("casting_1", ""),
                    'casting_2': request.POST.get("casting_2", ""),
                    'casting_3': request.POST.get("casting_3", ""),
                    'shrinkage_1': request.POST.get("shrinkage_1", ""),
                    'shrinkage_2': request.POST.get("shrinkage_2", ""),
                    'shrinkage_3': request.POST.get("shrinkage_3", ""),
                    'machining_1': request.POST.get("machining_1", ""),
                    'machining_2': request.POST.get("machining_2", ""),
                    'machining_3': request.POST.get("machining_3", ""),
                }
                 return render(request, template, context)

                                                    
        except Exception as e:
            steps = f"<span style='color:red;'>Unexpected server error: {str(e)}</span>"

    return render(request, template, {
        'experiment': experiment,
        'weights': weights,
        'result': result,
        'steps': steps,
        'weight_inputs': weight_inputs,
        'graph_data': graph_data,
        'email': email,
        'moisture_results':moisture_results  if moisture_results else [
            {"sample": i, "W1": "", "W2": "", "mc": ""} for i in range(1, 6)
        ],
        'W1':request.POST.get("W1",""),
        'W2':request.POST.get("W2",""),
        'gc_values':gc_values,
        'result_gc':result_gc,
        'result_shear':result_shear,
        'gc_trials':trials,
       'context':context,
       'dims':dims,
       'steps_html':steps_html,
       'table_html':table_html,
       'email_sent':email_sent,
          
                
    })
