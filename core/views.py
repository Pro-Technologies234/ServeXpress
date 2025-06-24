from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, Proposal, Category
from .forms import PostJobForm, JobProposalForm
from notification.models import Notification
from django.db.models import Count, Q


# Create your views here.
@login_required
def dashboard(request):
    if request.user.role == "freelancer":
        return redirect("find_jobs")
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    return render(request, "core/dashboard.html")

 
@login_required
def my_jobs(request):
    if request.user.role == "admin":
        return redirect("admin_dashboard")
    jobs = Job.objects.filter(client=request.user)
    categories = Category.objects.filter()
    if request.method == "POST":
        category = request.POST.getlist("categories")
        post_job_form = PostJobForm(request.POST)
        if post_job_form.is_valid():
            job = post_job_form.save(commit=False)
            job.client = request.user
            job.save()
            job.categories.set(category)
            job.save()
            messages.success(request,f"Your Job was Posted Successfully.")
            return redirect("my_jobs")
    else:
        post_job_form = PostJobForm()
    
    context = {
        "jobs" : jobs,
        "post_job_form": post_job_form,
        "categories": categories,
    }
    return render(request, "core/client/my_jobs.html", context)


@login_required
def find_jobs(request):
    # if request.user.role == "admin":
    #     return redirect("admin_dashboard")
    current_category = request.GET.get("category",0)
    categories = Category.objects.filter()
    selected_job_id = request.GET.get("selected_job_id")
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at")
    
    if selected_job_id:
        selected_job = get_object_or_404(Job,pk=selected_job_id)
    else:
        selected_job = None
        
    if not current_category:
        jobs = Job.objects.filter(is_assigned=False).order_by('-created_at')
    else:
        jobs = Job.objects.filter(categories=current_category,is_assigned=False).order_by('-created_at')
        
    if request.method == "POST":
        job_application_form = JobProposalForm(request.POST)
        
        proposal_sent = selected_job.proposals.filter(freelancer=request.user).exists()
        if proposal_sent:
            messages.error(request, f"You alread sent a Proposal for this Job #{selected_job.title}")
            return redirect(find_jobs)
        
        if job_application_form.is_valid():
            proposal = job_application_form.save(commit=False)
            proposal.freelancer = request.user
            proposal.job = selected_job
            proposal.save()
            messages.success(request,"Your Job Application has been sent Successfully and its waiting for review")
            return redirect('find_jobs')
    else:
        job_application_form = JobProposalForm()
        
        
    context = {
        "jobs" : jobs,
        "categories": categories,
        "current_category":int(current_category),
        "selected_job": selected_job,
        "job_application_form": job_application_form,
        "notifications": notifications,
    }
    return render(request, "core/freelancer/find_jobs.html", context)

@login_required
def proposals(request):
    not_accepted_proposals = Proposal.objects.filter(accepted=False)
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by("-created_at").order_by("-created_at").order_by("-created_at").order_by("-created_at").order_by("-created_at")
    jobs = Job.objects.filter(client=request.user)\
    .annotate(
        proposal_count=Count('proposals', filter=Q(proposals__accepted=False) | Q(proposals__accepted__isnull=True))
    )\
    .order_by('-proposal_count')
    current_job_id = request.GET.get("current_job_id")
    selected_proposal_id = request.GET.get('selected_proposal_id')
    if current_job_id:
        current_job_proposals = get_object_or_404(Job,id=current_job_id).proposals.filter(accepted=False)
    else: 
        first_job = Job.objects.first()
        if first_job:
            current_job_proposals = first_job.proposals.all()
        else:
            current_job_proposals = []  

    if selected_proposal_id:
        current_proposal = get_object_or_404(Proposal,id=selected_proposal_id)
    else:
        first_proposal = current_job_proposals.first()
        if first_proposal:
            current_proposal = get_object_or_404(Proposal,id=first_proposal.id)
        else:
            current_proposal = []

    context = {
        "notifications": notifications,
        "jobs": jobs,
        "current_job_id": current_job_id,
        "current_job_proposals": current_job_proposals,
        "selected_proposal_id":selected_proposal_id,
        "current_proposal": current_proposal,
        "not_accepted_proposals":not_accepted_proposals,
    }
    return render(request, "core/client/proposals.html", context)


def accept_proposal(request,proposal_id):
    accepted_proposal = get_object_or_404(Proposal,id=proposal_id)
    accepted_proposal.accepted = True
    accepted_proposal.job.is_assigned = True
    accepted_proposal.job.save()
    accepted_proposal.save()
    all_proposals = Proposal.objects.filter(job=accepted_proposal.job,accepted=False)
    
    for proposal in all_proposals:
        proposal.delete()
    
    messages.success(request,"You have Accepted a proposal for this freelancer.")
    return redirect("proposals")